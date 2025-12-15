#!/usr/bin/env python3
"""
Configuration validator for BLEUHeritage studies
"""

import yaml
import sys
import os
from pathlib import Path

class ConfigValidator:
    """Validate BLEUHeritage configuration files"""
    
    REQUIRED_SECTIONS = [
        'study',
        'metadata',
        'sampling',
        'genomics'
    ]
    
    REQUIRED_FIELDS = {
        'study': ['id', 'name', 'version'],
        'metadata': ['samplesheet', 'output_dir'],
        'sampling': ['method', 'preservation_method'],
        'genomics': ['reference', 'sequencing']
    }
    
    @staticmethod
    def validate_file(config_path):
        """Validate configuration YAML file"""
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return False, [f"YAML parsing error: {str(e)}"]
        
        errors = []
        warnings = []
        
        # Check required sections
        for section in ConfigValidator.REQUIRED_SECTIONS:
            if section not in config:
                errors.append(f"Missing required section: {section}")
        
        # Check required fields within sections
        for section, fields in ConfigValidator.REQUIRED_FIELDS.items():
            if section in config:
                for field in fields:
                    if field not in config[section]:
                        errors.append(f"Missing required field: {section}.{field}")
        
        # Validate specific values
        if 'study' in config:
            study = config['study']
            
            # Check study ID format
            if 'id' in study:
                study_id = study['id']
                if not study_id.startswith('BH-'):
                    warnings.append(f"Study ID '{study_id}' doesn't follow BLEUHeritage naming convention")
            
            # Check ethics
            if 'ethics' in study:
                ethics = study['ethics']
                if ethics.get('approved') is not True:
                    warnings.append("Ethics approval not marked as approved")
        
        # Check metadata file existence
        if 'metadata' in config:
            metadata = config['metadata']
            if 'samplesheet' in metadata:
                samplesheet = metadata['samplesheet']
                if not os.path.exists(samplesheet):
                    warnings.append(f"Samplesheet file not found: {samplesheet}")
        
        # Check genomic reference
        if 'genomics' in config:
            genomics = config['genomics']
            if 'reference' in genomics:
                ref = genomics['reference']
                if 'genome' in ref and not os.path.exists(ref['genome']):
                    warnings.append(f"Reference genome file not found: {ref['genome']}")
        
        # Check output directories
        if 'output' in config and 'directories' in config['output']:
            dirs = config['output']['directories']
            for name, path in dirs.items():
                if not os.path.exists(path):
                    warnings.append(f"Output directory doesn't exist: {path}")
        
        return len(errors) == 0, errors, warnings
    
    @staticmethod
    def generate_minimal_config(output_path):
        """Generate a minimal valid configuration template"""
        
        minimal_config = {
            'study': {
                'id': 'BH-STUDY-0001',
                'name': 'Your Study Name',
                'version': '1.0.0',
                'contact': {
                    'name': 'Researcher Name',
                    'email': 'research@institution.edu'
                }
            },
            'metadata': {
                'samplesheet': 'data/metadata/samples.csv',
                'output_dir': 'results/metadata/'
            },
            'sampling': {
                'method': 'nonlethal_leg_clip',
                'preservation_method': 'ethanol_95_100_percent'
            },
            'genomics': {
                'reference': {
                    'genome': 'path/to/reference.fasta'
                },
                'sequencing': {
                    'type': 'WGS',
                    'coverage': 10
                }
            }
        }
        
        with open(output_path, 'w') as f:
            yaml.dump(minimal_config, f, default_flow_style=False, sort_keys=False)
        
        print(f"Generated minimal configuration: {output_path}")
        return output_path

def main():
    """Command-line interface"""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Validate: python validate_config.py config.yaml")
        print("  Generate: python validate_config.py --generate template.yaml")
        sys.exit(1)
    
    if sys.argv[1] == '--generate':
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'minimal-config.yaml'
        ConfigValidator.generate_minimal_config(output_file)
    else:
        config_file = sys.argv[1]
        
        if not os.path.exists(config_file):
            print(f"Error: Configuration file not found: {config_file}")
            sys.exit(1)
        
        is_valid, errors, warnings = ConfigValidator.validate_file(config_file)
        
        print(f"Validating: {config_file}")
        print("=" * 50)
        
        if is_valid:
            print("✅ Configuration is VALID")
        else:
            print("❌ Configuration has ERRORS")
        
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for error in errors:
                print(f"  - {error}")
        
        if warnings:
            print(f"\nWarnings ({len(warnings)}):")
            for warning in warnings:
                print(f"  ⚠️  {warning}")
        
        if not errors and not warnings:
            print("\nNo issues found. Configuration is ready to use.")
        
        sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()
