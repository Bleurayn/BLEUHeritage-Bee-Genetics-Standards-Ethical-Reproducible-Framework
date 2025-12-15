#!/usr/bin/env python3
"""
Automated Zenodo deposit script
Run on GitHub release
"""

import os
import json
import requests
import yaml
from pathlib import Path

def create_zenodo_deposit():
    """Create a new deposit on Zenodo"""
    
    # Configuration
    ZENODO_URL = "https://zenodo.org"
    if os.getenv('ZENODO_SANDBOX', 'false').lower() == 'true':
        ZENODO_URL = "https://sandbox.zenodo.org"
        print("Using Zenodo Sandbox for testing")
    
    ACCESS_TOKEN = os.getenv('ZENODO_TOKEN')
    if not ACCESS_TOKEN:
        raise ValueError("ZENODO_TOKEN environment variable required")
    
    # Get release information from GitHub environment
    github_ref = os.getenv('GITHUB_REF', '')
    release_tag = github_ref.replace('refs/tags/', '')
    repo = os.getenv('GITHUB_REPOSITORY', 'bleuheritage/standards')
    
    print(f"Creating deposit for release: {release_tag}")
    print(f"Repository: {repo}")
    
    # Load metadata from .zenodo.json
    with open('.zenodo.json', 'r') as f:
        metadata = json.load(f)
    
    # Update metadata with release info
    metadata['version'] = release_tag
    metadata['related_identifiers'].append({
        "relation": "isVersionOf",
        "identifier": f"https://github.com/{repo}"
    })
    
    # Get files to upload (excluding .git, large files)
    files_to_upload = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and .git
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.startswith('.'):
                continue
            
            filepath = Path(root) / file
            # Skip large files and binaries
            if filepath.stat().st_size > 100 * 1024 * 1024:  # 100MB
                print(f"Skipping large file: {filepath}")
                continue
            
            # Skip certain file types
            if filepath.suffix.lower() in ['.pyc', '.so', '.dll', '.exe']:
                continue
            
            files_to_upload.append(str(filepath))
    
    print(f"Found {len(files_to_upload)} files to upload")
    
    # Create deposit
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    # Step 1: Create empty deposit
    print("Creating deposit...")
    response = requests.post(
        f"{ZENODO_URL}/api/deposit/depositions",
        params={"access_token": ACCESS_TOKEN},
        json={},
        headers=headers
    )
    
    if response.status_code != 201:
        print(f"Error creating deposit: {response.status_code}")
        print(response.text)
        return None
    
    deposit = response.json()
    deposit_id = deposit['id']
    print(f"Deposit created with ID: {deposit_id}")
    
    # Step 2: Upload files
    bucket_url = deposit['links']['bucket']
    
    for filepath in files_to_upload:
        try:
            print(f"Uploading: {filepath}")
            
            with open(filepath, 'rb') as f:
                filename = os.path.basename(filepath)
                upload_url = f"{bucket_url}/{filename}"
                
                response = requests.put(
                    upload_url,
                    data=f,
                    params={"access_token": ACCESS_TOKEN}
                )
                
                if response.status_code != 200:
                    print(f"  Failed to upload {filepath}: {response.status_code}")
                else:
                    print(f"  ✓ Uploaded {filepath}")
                    
        except Exception as e:
            print(f"  Error uploading {filepath}: {str(e)}")
    
    # Step 3: Update metadata
    print("Updating metadata...")
    response = requests.put(
        f"{ZENODO_URL}/api/deposit/depositions/{deposit_id}",
        params={"access_token": ACCESS_TOKEN},
        data=json.dumps({"metadata": metadata}),
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"Error updating metadata: {response.status_code}")
        print(response.text)
        return None
    
    print("Metadata updated successfully")
    
    # Step 4: Publish deposit
    print("Publishing deposit...")
    response = requests.post(
        f"{ZENODO_URL}/api/deposit/depositions/{deposit_id}/actions/publish",
        params={"access_token": ACCESS_TOKEN},
        headers=headers
    )
    
    if response.status_code != 202:
        print(f"Error publishing deposit: {response.status_code}")
        print(response.text)
        
        # If publish failed, save as draft
        print("Saving as draft instead...")
        return deposit.get('links', {}).get('html', '')
    
    published_deposit = response.json()
    doi = published_deposit.get('doi', 'Not assigned yet')
    doi_url = published_deposit.get('links', {}).get('doi', '')
    
    print(f"✅ Deposit published successfully!")
    print(f"📄 DOI: {doi}")
    print(f"🔗 URL: {doi_url}")
    
    # Output for GitHub Actions
    if os.getenv('GITHUB_ACTIONS'):
        print(f"::set-output name=doi::{doi}")
        print(f"::set-output name=doi_url::{doi_url}")
        print(f"::set-output name=deposit_id::{deposit_id}")
    
    return doi_url

if __name__ == "__main__":
    try:
        doi_url = create_zenodo_deposit()
        if doi_url:
            print(f"\n🎉 Success! View your deposit at: {doi_url}")
        else:
            print("\n❌ Deposit creation failed")
            exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        exit(1)
