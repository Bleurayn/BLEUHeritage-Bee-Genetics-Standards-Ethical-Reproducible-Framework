# BLEUHeritage Bee Genetics Standards & Protocols

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Standard Status](https://img.shields.io/badge/status-production-blue)](https://bleuheritage.org)

## Overview

Standardized framework for bee genetics research with integrated ethical governance, data privacy, and reproducible science practices. This repository contains the open standards, protocols, and documentation for the BLEUHeritage Bee Genetics Study framework.

## What This Includes

### 🗃️ Metadata Standards
- Complete JSON schema for bee genetics metadata
- Validation rules for data quality
- Data dictionary with field definitions

### 📋 Field Protocols
- Non-lethal sampling methods
- Chain of custody procedures
- Ethical collection guidelines

### ⚖️ Governance Framework
- Data sovereignty principles
- Tiered data access model
- Community engagement protocols

### 🧪 Example Implementations
- Sample metadata files
- Configuration examples
- Validation scripts

## Quick Start

### For Researchers
1. Review the [field protocols](protocols/field-collection-protocol.md)
2. Use the [metadata schema](schema/metadata-schema.json) for your study
3. Validate data with our [validation rules](schema/validation-rules.json)

### For Developers
```bash
# Clone repository
git clone https://github.com/bleuheritage/standards.git

# Validate sample metadata
python examples/validation-example.py examples/sample-metadata.csv
