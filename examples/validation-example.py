#!/usr/bin/env python3
"""
Simple validation example for BLEUHeritage metadata
This is a reference implementation - full validation available commercially
"""

import json
import csv
import re
from datetime import datetime

def validate_sample_metadata(csv_path):
    """Basic validation of sample metadata CSV"""
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        samples = list(reader)
    
    errors = []
    warnings = []
    
    # Patterns from schema
    patterns = {
        'study_id': r'^[A-Z]{2,4}-[A-Z]{6,8}-[0-9]{4}$',
        'site_id': r'^SITE-[A-Z0-9]{4,12}$',
        'sample_id': r'^[A-Z]{2,4}-[A-Z]{6,8}-[0-9]{4}-[A-Z0-9]{1,6}-SITE-[A-Z0-9]{4,12}-[0-9]{8}-[0-9]{3}$',
        'coc_id': r'^COC-[A-Z0-9]{8,20}$'
    }
    
    for i, sample in enumerate(samples, 1):
        row_num = i + 1  # Account for header
        
        # Check required fields
        required = ['study_id', 'site_id', 'sample_id', 'collection_date']
        for field in required:
            if not sample.get(field):
                errors.append(f"Row {row_num}: Missing required field '{field}'")
        
        # Check pattern matches
        for field, pattern in patterns.items():
            if field in sample and sample[field]:
                if not re.match(pattern, sample[field]):
                    errors.append(f"Row {row_num}: Invalid format for {field}: {sample[field]}")
        
        # Check collection date not in future
        if sample.get('collection_date'):
            try:
                coll_date = datetime.strptime(sample['collection_date'], '%Y-%m-%d').date()
                if coll_date > datetime.now().date():
                    errors.append(f"Row {row_num}: Collection date in future: {sample['collection_date']}")
            except ValueError:
                errors.append(f"Row {row_num}: Invalid date format: {sample['collection_date']}")
    
    # Print results
    print(f"Validated {len(samples)} samples")
    
    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
    else:
        print("✅ No validation errors")
    
    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for warning in warnings[:5]:
            print(f"  - {warning}")
    
    return len(errors) == 0

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python validation-example.py <metadata.csv>")
        sys.exit(1)
    
    success = validate_sample_metadata(sys.argv[1])
    sys.exit(0 if success else 1)
