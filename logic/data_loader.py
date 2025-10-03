"""
Data Loader Module
Handles loading and cleaning of all input data files
"""

import pandas as pd
import config

class DataLoader:
    """
    Loads and cleans all input Excel files for ISRR analysis
    """
    
    def __init__(self):
        self.variables_df = None
        self.rfimapped_df = None
        self.mainrfi_df = None
        self.interimisrr_df = None
        self.finalisrr_df = None
        self.egid_column = None
        
    def load_all_files(self):
        """Load all required Excel files"""
        print("="*70)
        print("LOADING DATA FILES")
        print("="*70)
        
        # Load variables
        print(f"\n1. Loading {config.INPUT_FILES['variables']}...")
        self.variables_df = pd.read_excel(config.INPUT_FILES['variables'])
        print(f"   ✓ Loaded {len(self.variables_df)} variables")
        
        # Load RFI mapped
        print(f"\n2. Loading {config.INPUT_FILES['rfimapped']}...")
        self.rfimapped_df = pd.read_excel(config.INPUT_FILES['rfimapped'])
        print(f"   ✓ Loaded {len(self.rfimapped_df)} records")
        
        # Load main RFI
        print(f"\n3. Loading {config.INPUT_FILES['mainrfi']}...")
        self.mainrfi_df = pd.read_excel(config.INPUT_FILES['mainrfi'])
        print(f"   ✓ Loaded {len(self.mainrfi_df)} records")
        
        # Load interim ISRR rules
        print(f"\n4. Loading {config.INPUT_FILES['interimisrr']}...")
        self.interimisrr_df = pd.read_excel(config.INPUT_FILES['interimisrr'])
        print(f"   ✓ Loaded {len(self.interimisrr_df)} rules")
        
        # Load final ISRR rules
        print(f"\n5. Loading {config.INPUT_FILES['finalisrr']}...")
        self.finalisrr_df = pd.read_excel(config.INPUT_FILES['finalisrr'])
        print(f"   ✓ Loaded {len(self.finalisrr_df)} rules")
        
        print("\n✓ All files loaded successfully!")
        
    def identify_egid_column(self):
        """Identify the EGID column in rfimapped dataset"""
        print("\n" + "="*70)
        print("IDENTIFYING EGID COLUMN")
        print("="*70)
        
        for col in config.EGID_COLUMN_VARIATIONS:
            if col in self.rfimapped_df.columns:
                self.egid_column = col
                print(f"✓ Found EGID column: '{self.egid_column}'")
                return self.egid_column
        
        # Fallback to first column
        self.egid_column = self.rfimapped_df.columns[0]
        print(f"⚠️ Standard EGID column not found. Using first column: '{self.egid_column}'")
        return self.egid_column
    
    def clean_rfimapped_data(self):
        """Clean and standardize rfimapped dataset"""
        print("\n" + "="*70)
        print("CLEANING RFIMAPPED DATA")
        print("="*70)
        
        original_count = len(self.rfimapped_df)
        
        # Strip whitespace from EGID
        if config.STRIP_WHITESPACE:
            print("\n1. Stripping whitespace from EGIDs...")
            self.rfimapped_df[self.egid_column] = self.rfimapped_df[self.egid_column].astype(str).str.strip()
            print("   ✓ Whitespace removed")
        
        # Remove null/empty EGIDs
        if config.REMOVE_NULL_EGIDS:
            print("\n2. Removing null/empty EGIDs...")
            self.rfimapped_df = self.rfimapped_df[self.rfimapped_df[self.egid_column].notna()]
            self.rfimapped_df = self.rfimapped_df[self.rfimapped_df[self.egid_column] != 'nan']
            self.rfimapped_df = self.rfimapped_df[self.rfimapped_df[self.egid_column] != '']
            
            removed = original_count - len(self.rfimapped_df)
            if removed > 0:
                print(f"   ⚠️ Removed {removed} rows with null/empty EGIDs")
            else:
                print("   ✓ No null/empty EGIDs found")
        
        # Handle duplicates
        if config.REMOVE_DUPLICATES:
            print("\n3. Checking for duplicate EGIDs...")
            duplicates = self.rfimapped_df[self.egid_column].duplicated().sum()
            
            if duplicates > 0:
                print(f"   ⚠️ Found {duplicates} duplicate EGIDs")
                print("   Keeping first occurrence of each duplicate...")
                self.rfimapped_df = self.rfimapped_df.drop_duplicates(subset=[self.egid_column], keep='first')
                print(f"   ✓ Removed {duplicates} duplicates")
            else:
                print("   ✓ No duplicates found")
        
        final_count = len(self.rfimapped_df)
        print(f"\n✓ Cleaning complete: {original_count} → {final_count} records")
        
    def clean_mainrfi_data(self):
        """Clean and standardize mainrfi dataset"""
        print("\n" + "="*70)
        print("CLEANING MAINRFI DATA")
        print("="*70)
        
        # Clean EGID columns
        print("\nStandardizing EGID columns...")
        for col in config.EGID_COLUMN_VARIATIONS:
            if col in self.mainrfi_df.columns:
                self.mainrfi_df[col] = self.mainrfi_df[col].astype(str).str.strip()
                print(f"   ✓ Cleaned column: '{col}'")
        
        print("✓ mainrfi data cleaned")
    
    def get_summary(self):
        """Return summary of loaded data"""
        summary = {
            'variables_count': len(self.variables_df),
            'rfimapped_records': len(self.rfimapped_df),
            'unique_egids': self.rfimapped_df[self.egid_column].nunique(),
            'mainrfi_records': len(self.mainrfi_df),
            'interim_rules': len(self.interimisrr_df),
            'final_rules': len(self.finalisrr_df),
            'egid_column': self.egid_column
        }
        return summary
    
    def print_summary(self):
        """Print data loading summary"""
        summary = self.get_summary()
        
        print("\n" + "="*70)
        print("DATA LOADING SUMMARY")
        print("="*70)
        print(f"Variables: {summary['variables_count']}")
        print(f"RFI Mapped Records: {summary['rfimapped_records']}")
        print(f"Unique EGIDs: {summary['unique_egids']}")
        print(f"Main RFI Records: {summary['mainrfi_records']}")
        print(f"Interim ISRR Rules: {summary['interim_rules']}")
        print(f"Final ISRR Rules: {summary['final_rules']}")
        print(f"EGID Column Name: '{summary['egid_column']}'")
        print("="*70)
