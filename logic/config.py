"""
Configuration file for ISRR Analysis
Contains all file paths, column mappings, and constants
"""

import os

# ============================================================================
# FILE PATHS
# ============================================================================

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# Create results directory if it doesn't exist
os.makedirs(RESULTS_DIR, exist_ok=True)

INPUT_FILES = {
    'variables': os.path.join(DATA_DIR, 'variables.xlsx'),
    'rfimapped': os.path.join(DATA_DIR, 'rifmapped.xlsx'),
    'mainrfi': os.path.join(DATA_DIR, 'mainrfi.xlsx'),
    'interimisrr': os.path.join(DATA_DIR, 'interimisrr.xlsx'),
    'finalisrr': os.path.join(DATA_DIR, 'finalisrr.xlsx')
}

OUTPUT_FILES = {
    'complete_analysis': 'complete_isrr_analysis.xlsx',
    'mismatches': 'isrr_mismatches.xlsx',
    'summary_report': 'isrr_summary_report.txt'
}

# ============================================================================
# COLUMN MAPPINGS
# ============================================================================

# Possible EGID column names (will try in order)
EGID_COLUMN_VARIATIONS = [
    'EGID', 'egid', 'Egid', 'EgId', 
    'Engagementid', 'EngagementId', 'engagement_id'
]

# Variables.xlsx columns
VARIABLES_COLUMNS = {
    'name': 'variables',
    'group': 'group',
    'type': 'type',
    'category': 'category',
    'classification': 'data_classification'
}

# MainRFI.xlsx columns
MAINRFI_COLUMNS = {
    'volume': 'Tpmaxrecordscanprocess',
    'format': 'Isdataelecform',
    'connectivity': 'Systemconnectivity',
    'existing_isrr': 'Isrrvalue',
    'generated_isrr': 'Generatedisrrvalue'
}

# InterimISRR.xlsx columns
INTERIM_ISRR_COLUMNS = {
    'nature_of_data': 'Nature of Data',
    'bank_data': 'Bank Data',
    'highest_classification': 'Highest Classification',
    'availability': 'Availability',
    'interim_isrr': 'Interim ISRR'
}

# FinalISRR.xlsx columns
FINAL_ISRR_COLUMNS = {
    'modifier': 'Modifier',
    'volume': 'Volume',
    'format': 'Data format',
    'connectivity': 'System Connectivity',
    'final_isrr': 'Final ISRR'
}

# ============================================================================
# RISK RATING MAPPINGS
# ============================================================================

# ISRR level to numeric mapping (for modifier calculations)
ISRR_TO_NUMBER = {
    'Minor': 1,
    'Low': 2,
    'Moderate': 3,
    'High': 4,
    'Critical': 5
}

# Numeric to ISRR level mapping
NUMBER_TO_ISRR = {
    1: 'Minor',
    2: 'Low',
    3: 'Moderate',
    4: 'High',
    5: 'Critical'
}

# Risk level priority (higher = more critical)
RISK_LEVEL_PRIORITY = {
    'Minor': 1,
    'Low': 2,
    'Moderate': 3,
    'High': 4,
    'Critical': 5
}

# ============================================================================
# DATA STANDARDIZATION MAPPINGS
# ============================================================================

# Volume categories
VOLUME_MAPPINGS = {
    '<10': '<10',
    '< 10': '<10',
    '<50': '<50',
    '< 50': '<50',
    '<100': '<100',
    '< 100': '<100',
    '10-49': '10-49',
    '10 - 49': '10-49'
}

# Format categories
FORMAT_MAPPINGS = {
    'electronic': 'Electronic',
    'hardcopy': 'Hardcopy',
    'hard copy': 'Hardcopy'
}

# Connectivity categories
CONNECTIVITY_MAPPINGS = {
    'privileged database access': 'Privileged database access'
}

# ============================================================================
# BUSINESS RULES
# ============================================================================

# Bank data classification rules
BANK_DATA_RULES = {
    'D4': ['personal_identifiable_information', 'employee_data'],  # Both must be present
    'D3': ['transactional_data'],  # Must be present
    'D2': ['personal_identifiable_information']  # Must be present
}

# Classification hierarchy (highest to lowest)
CLASSIFICATION_HIERARCHY = [
    'Restricted',
    'Confidential',
    'Internal / Confidential'
]

# ============================================================================
# PROCESSING SETTINGS
# ============================================================================

# Progress reporting interval (print status every N records)
PROGRESS_INTERVAL = 50

# Maximum number of sample results to display
MAX_SAMPLE_DISPLAY = 5

# Enable/disable verbose logging
VERBOSE_MODE = True

# ============================================================================
# VALIDATION SETTINGS
# ============================================================================

# Whether to remove duplicate EGIDs (keep first occurrence)
REMOVE_DUPLICATES = True

# Whether to remove null/empty EGIDs
REMOVE_NULL_EGIDS = True

# Whether to strip whitespace from EGIDs
STRIP_WHITESPACE = True

# ============================================================================
# EXPORT SETTINGS
# ============================================================================

# Columns to include in final export
EXPORT_COLUMNS = [
    'EGID',
    'Existing_ISRR_Value',
    'Calculated_Interim_ISRR',
    'Calculated_Final_ISRR',
    'ISRR_Match',
    'Calculation_vs_Existing',
    'Interim_to_Final_Change',
    'Nature_of_Data',
    'Bank_Data',
    'Highest_Classification',
    'Availability',
    'Volume',
    'Format',
    'Connectivity',
    'Modifier_Applied',
    'Transactional_Groups',
    'Non_Transactional_Groups',
    'Interim_Rule_Matched',
    'Final_Rule_Matched'
]

# Columns to include in mismatch export
MISMATCH_COLUMNS = [
    'EGID',
    'Existing_ISRR',
    'Calculated_Final_ISRR',
    'Difference'
]
