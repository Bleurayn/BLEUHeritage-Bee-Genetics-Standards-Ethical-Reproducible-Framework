# BLEUHeritage Bee Genetics Data Dictionary
## Version 1.0.0
## Last Updated: December 2025

## Overview
This data dictionary defines all fields in the BLEUHeritage Bee Genetics metadata schema. Each field includes type information, validation rules, privacy classification, and usage guidelines.

## Field Classification System

### Privacy Tiers
- **Tier 1 (PUBLIC)**: Can be shared openly in publications and public repositories
- **Tier 2 (COLLABORATOR)**: Shared with research partners under data use agreements
- **Tier 3 (INTERNAL_ONLY)**: Never shared externally; used for internal tracking only

### Data Sensitivity Levels
- **LOW**: No privacy or security concerns (e.g., study ID, method descriptions)
- **MEDIUM**: Requires some protection (e.g., generalized locations, aggregated data)
- **HIGH**: Requires strict protection (e.g., exact coordinates, personal identifiers)

## Study-Level Metadata

| Field Name | Type | Required | Pattern/Values | Description | Privacy Tier | Sensitivity |
|------------|------|----------|----------------|-------------|--------------|-------------|
| `study_id` | String | Yes | `^[A-Z]{2,4}-[A-Z]{6,8}-[0-9]{4}$` | Unique study identifier following BLEUHeritage naming convention | PUBLIC | LOW |
| `study_title` | String | Yes | Max 200 chars | Descriptive title of the research study | PUBLIC | LOW |
| `study_description` | String | No | Max 1000 chars | Brief overview of study objectives and methods | PUBLIC | LOW |
| `principal_investigator` | String | Yes | Max 100 chars | Name of study lead researcher | COLLABORATOR | MEDIUM |
| `institution` | String | Yes | Max 150 chars | Primary research institution | PUBLIC | LOW |
| `funding_source` | String | No | Max 200 chars | Grant numbers or funding agencies | PUBLIC | LOW |
| `ethics_approval_id` | String | Yes | `^[A-Z]{2,6}-[0-9]{4}-[0-9]{3,6}$` | Institutional review board approval identifier | INTERNAL_ONLY | HIGH |
| `study_start_date` | Date | Yes | YYYY-MM-DD | Official start date of study | PUBLIC | LOW |
| `study_end_date` | Date | No | YYYY-MM-DD | Planned or actual end date | PUBLIC | LOW |

## Site-Level Metadata

| Field Name | Type | Required | Pattern/Values | Description | Privacy Tier | Sensitivity |
|------------|------|----------|----------------|-------------|--------------|-------------|
| `site_id` | String | Yes | `^SITE-[A-Z0-9]{4,12}$` | Unique site identifier | PUBLIC (masked) | MEDIUM |
| `region_id` | String | Yes | `^R[0-9]{1,2}$` | Geographic region code | PUBLIC | LOW |
| `site_type` | String | Yes | `managed_apiary`, `wild_or_feral_colony`, `urban_corridor`, `agricultural_zone` | Classification of collection site | PUBLIC | LOW |
| `general_location` | String | Yes | Max 120 chars | Generalized location description (region-level only) | PUBLIC | LOW |
| `habitat_type` | String | Yes | Max 80 chars | Broad habitat classification | PUBLIC | LOW |
| `land_use_context` | String | No | Max 120 chars | Surrounding land use (agricultural, urban, forest, etc.) | COLLABORATOR | MEDIUM |
| `management_practices` | String | No | Max 600 chars | Summary of apiary management practices if applicable | COLLABORATOR | MEDIUM |
| `pesticide_exposure_proxy` | String | No | Max 200 chars | Indicator of potential pesticide exposure | COLLABORATOR | MEDIUM |
| `flora_resources` | String | No | Max 400 chars | Notes on floral resources available | COLLABORATOR | MEDIUM |
| `climate_zone` | String | No | Max 80 chars | Köppen-Geiger or similar climate classification | PUBLIC | LOW |
| `consent_id` | String | Yes | `^CONSENT-[A-Z0-9]{6,18}$` | Reference to consent documentation | INTERNAL_ONLY | HIGH |
| `sensitive_location_ref` | String | No | `^LOCREF-[A-Z0-9]{8,20}$` | Pointer to exact coordinates in internal-only table | INTERNAL_ONLY | HIGH |

## Colony-Level Metadata (Optional)

| Field Name | Type | Required | Pattern/Values | Description | Privacy Tier | Sensitivity |
|------------|------|----------|----------------|-------------|--------------|-------------|
| `colony_id` | String | Yes* | `^COL-[A-Z0-9]{4,14}$` | Unique colony identifier | COLLABORATOR | MEDIUM |
| `colony_origin_known` | Boolean | Yes | `true`/`false` | Whether colony origin/source is documented | COLLABORATOR | MEDIUM |
| `queen_source` | String | No | Max 140 chars | Information about queen origin if known | COLLABORATOR | MEDIUM |
| `colony_age_months` | Integer | No | 0-240 | Estimated age of colony in months | COLLABORATOR | MEDIUM |
| `health_score` | Number | No | 0.0-10.0 | Subjective or measured health assessment | COLLABORATOR | MEDIUM |
| `disease_signs` | String | No | Max 240 chars | Observed signs of disease or parasites | COLLABORATOR | MEDIUM |
| `treatment_history` | String | No | Max 500 chars | Record of treatments applied to colony | COLLABORATOR | MEDIUM |

*Required only if tracking individual colonies

## Sample-Level Metadata

| Field Name | Type | Required | Pattern/Values | Description | Privacy Tier | Sensitivity |
|------------|------|----------|----------------|-------------|--------------|-------------|
| `sample_id` | String | Yes | Complex pattern (see below) | Unique sample identifier | PUBLIC (masked) | MEDIUM |
| `collector_id` | String | Yes | `^P-[A-Z0-9]{3,18}$` | Identifier of person who collected sample | INTERNAL_ONLY | HIGH |
| `collection_date` | Date | Yes | YYYY-MM-DD | Date sample was collected | PUBLIC | LOW |
| `collection_time` | Time | No | HH:MM (24h) | Time of collection (optional) | COLLABORATOR | MEDIUM |
| `collection_method` | String | Yes | `worker_bee_collection`, `nonlethal_leg_clip`, `swarm_collection` | Specific method used for collection | PUBLIC | LOW |
| `life_stage` | String | Yes | `adult_worker`, `adult_drone`, `queen`, `larva` | Developmental stage at collection | PUBLIC | LOW |
| `preservation_method` | String | Yes | `ethanol_95_100_percent`, `RNAlater`, `dry_ice`, `liquid_nitrogen` | Method used for sample preservation | PUBLIC | LOW |
| `storage_temperature_c` | Number | Yes | -196 to 25 | Temperature at which sample is stored | INTERNAL_ONLY | MEDIUM |
| `storage_location` | String | Yes | Max 120 chars | Physical storage location (freezer/shelf) | INTERNAL_ONLY | MEDIUM |
| `coc_id` | String | Yes | `^COC-[A-Z0-9]{8,20}$` | Chain of Custody identifier | INTERNAL_ONLY | HIGH |
| `photo_references` | Array | No | Array of strings | File references to photographic evidence | INTERNAL_ONLY | MEDIUM |
| `sample_notes` | String | No | Max 800 chars | Free-text notes about the sample | COLLABORATOR | MEDIUM |
| `sample_status` | String | Yes | `PLANNED`, `COLLECTED`, `IN_TRANSIT`, `RECEIVED`, `EXTRACTED`, `LIB_PREPPED`, `SEQUENCED`, `QC_FAILED`, `ARCHIVED` | Current status in processing pipeline | INTERNAL_ONLY | LOW |

## Laboratory Processing Metadata

| Field Name | Type | Required | Pattern/Values | Description | Privacy Tier | Sensitivity |
|------------|------|----------|----------------|-------------|--------------|-------------|
| `extraction_date` | Date | No | YYYY-MM-DD | Date DNA/RNA was extracted | COLLABORATOR | MEDIUM |
| `extraction_method` | String | No | `column_kit`, `magnetic_beads`, `phenol_chloroform` | DNA extraction protocol used | COLLABORATOR | MEDIUM |
| `extraction_technician` | String | No | `^T-[A-Z0-9]{3,12}$` | Identifier of lab technician | INTERNAL_ONLY | HIGH |
| `dna_concentration_ng_ul` | Number | No | >0 | DNA concentration in ng/μL | COLLABORATOR | MEDIUM |
| `dna_quality_260_280` | Number | No | 1.7-2.2 | 260/280 absorbance ratio | COLLABORATOR | MEDIUM |
| `library_prep_date` | Date | No | YYYY-MM-DD | Date sequencing library was prepared | COLLABORATOR | MEDIUM |
| `library_type` | String | No | `WGS`, `RADseq`, `targeted`, `RNAseq` | Type of sequencing library | PUBLIC | LOW |
| `sequencing_run_id` | String | No | `^RUN-[A-Z0-9]{6,16}$` | Identifier for sequencing run | COLLABORATOR | MEDIUM |

## Genomic Analysis Metadata

| Field Name | Type | Required | Pattern/Values | Description | Privacy Tier | Sensitivity |
|------------|------|----------|----------------|-------------|--------------|-------------|
| `raw_read_count` | Integer | No | >0 | Number of raw sequencing reads | COLLABORATOR | MEDIUM |
| `mean_coverage` | Number | No | >0 | Average read depth across genome | PUBLIC | LOW |
| `coverage_sd` | Number | No | >0 | Standard deviation of coverage | COLLABORATOR | MEDIUM |
| `mapping_rate` | Number | No | 0-100 | Percentage of reads mapped to reference | COLLABORATOR | MEDIUM |
| `variant_count` | Integer | No | >0 | Number of variants called for sample | COLLABORATOR | MEDIUM |
| `heterozygosity` | Number | No | 0-1 | Observed heterozygosity | PUBLIC | LOW |
| `relatedness_flag` | String | No | `SIBLING`, `PARENT_OFFSPRING`, `UNRELATED` | Relatedness to other samples in study | COLLABORATOR | MEDIUM |
| `contamination_flag` | Boolean | No | `true`/`false` | Indication of potential contamination | INTERNAL_ONLY | HIGH |

## Special Note on Sample ID Pattern
The `sample_id` field follows this complex pattern:
