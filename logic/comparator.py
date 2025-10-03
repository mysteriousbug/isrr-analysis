"""
Comparator Module
Compares calculated ISRR with existing values and generates reports
"""

import pandas as pd
import os
from collections import defaultdict
import config

class ISRRComparator:
    """
    Compares calculated final ISRR with existing ISRR values
    """
    
    def __init__(self, mainrfi_df, egid_column):
        self.mainrfi_df = mainrfi_df
        self.egid_column = egid_column
        self.results_df = None
        self.mismatches_df = None
        
    def compare_results(self, egid_analysis, interim_results, final_results):
        """Compare calculated results with existing ISRR values"""
        print("\n" + "="*70)
        print("STEP 4: COMPARISON WITH EXISTING ISRR VALUES")
        print("="*70)
        
        results_data = []
        comparison_mismatches = []
        
        egids = list(final_results.keys())
        print(f"\nComparing results for {len(egids)} EGIDs...")
        
        for egid in egids:
            interim_data = interim_results[egid]
            final_data = final_results[egid]
            analysis_data = egid_analysis[egid]
            
            # Get existing ISRR value from mainrfi
            existing_isrr = self._get_existing_isrr(egid)
            
            # Check if calculated and existing ISRR match
            calculated_final = final_data['final_isrr']
            isrr_match = (calculated_final.lower() == existing_isrr.lower())
            
            if not isrr_match and existing_isrr not in ['Not Found', 'Not Available']:
                comparison_mismatches.append({
                    'EGID': egid,
                    'Existing_ISRR': existing_isrr,
                    'Calculated_Final_ISRR': calculated_final,
                    'Difference': f"{existing_isrr} → {calculated_final}"
                })
            
            results_data.append({
                'EGID': egid,
                'Existing_ISRR_Value': existing_isrr,
                'Calculated_Interim_ISRR': interim_data['interim_isrr'],
                'Calculated_Final_ISRR': final_data['final_isrr'],
                'ISRR_Match': 'Yes' if isrr_match else 'No',
                'Calculation_vs_Existing': f"{existing_isrr} vs {calculated_final}",
                'Interim_to_Final_Change': 'Yes' if interim_data['interim_isrr'] != final_data['final_isrr'] else 'No',
                'Nature_of_Data': interim_data['nature_of_data'],
                'Bank_Data': interim_data['bank_data'],
                'Highest_Classification': interim_data['highest_classification'],
                'Availability': interim_data['availability'],
                'Volume': final_data['volume'],
                'Format': final_data['format'],
                'Connectivity': final_data['connectivity'],
                'Modifier_Applied': final_data['modifier_applied'],
                'Transactional_Groups': len(interim_data['data_groups_info']['transactional_groups']),
                'Non_Transactional_Groups': len(interim_data['data_groups_info']['non_transactional_groups']),
                'Interim_Rule_Matched': interim_data.get('matched_rule', 'Unknown'),
                'Final_Rule_Matched': final_data.get('matched_rule', 'Unknown')
            })
        
        self.results_df = pd.DataFrame(results_data)
        self.mismatches_df = pd.DataFrame(comparison_mismatches)
        
        self._print_comparison_summary()
        
        return self.results_df, self.mismatches_df
    
    def _get_existing_isrr(self, egid):
        """Get existing ISRR value for an EGID from mainrfi"""
        mainrfi_row = None
        
        for col in config.EGID_COLUMN_VARIATIONS:
            if col in self.mainrfi_df.columns:
                matching_rows = self.mainrfi_df[self.mainrfi_df[col] == egid]
                if not matching_rows.empty:
                    mainrfi_row = matching_rows.iloc[0]
                    break
        
        if mainrfi_row is None:
            return 'Not Found'
        
        # Try to get ISRR value
        isrr_value = mainrfi_row.get(config.MAINRFI_COLUMNS['existing_isrr'])
        
        if pd.isna(isrr_value):
            return 'Not Available'
        
        return str(isrr_value).strip()
    
    def _print_comparison_summary(self):
        """Print comparison summary statistics"""
        total_egids = len(self.results_df)
        total_mismatches = len(self.mismatches_df)
        match_rate = ((total_egids - total_mismatches) / total_egids * 100) if total_egids > 0 else 0
        
        print(f"\nTotal EGIDs processed: {total_egids}")
        print(f"EGIDs with existing ISRR values: {len(self.results_df[self.results_df['Existing_ISRR_Value'].isin(['Not Found', 'Not Available']) == False])}")
        print(f"EGIDs with mismatched ISRR: {total_mismatches}")
        print(f"Match rate: {match_rate:.1f}%")
        
        if total_mismatches > 0:
            print("\n" + "="*70)
            print("🚨 ISRR MISMATCHES DETECTED")
            print("="*70)
            
            # Analyze mismatch patterns
            if 'Difference' in self.mismatches_df.columns:
                mismatch_patterns = self.mismatches_df['Difference'].value_counts()
                print(f"\nTop mismatch patterns:")
                for pattern, count in mismatch_patterns.head(10).items():
                    print(f"  {pattern}: {count} occurrences")
            
            # Show sample mismatches
            print(f"\nSample mismatches (first 10):")
            for i, row in self.mismatches_df.head(10).iterrows():
                print(f"  EGID {row['EGID']}: {row['Existing_ISRR']} → {row['Calculated_Final_ISRR']}")
            
            # Analyze mismatch severity
            self._analyze_mismatch_severity()
        else:
            print("\n✅ ALL ISRR VALUES MATCH! No discrepancies found.")
    
    def _analyze_mismatch_severity(self):
        """Analyze the severity of mismatches"""
        print(f"\nMismatch severity analysis:")
        
        risk_levels = ['Minor', 'Low', 'Moderate', 'High', 'Critical']
        severity_increases = 0
        severity_decreases = 0
        
        for _, row in self.mismatches_df.iterrows():
            existing = row['Existing_ISRR']
            calculated = row['Calculated_Final_ISRR']
            
            if existing in risk_levels and calculated in risk_levels:
                existing_idx = risk_levels.index(existing)
                calculated_idx = risk_levels.index(calculated)
                
                if calculated_idx > existing_idx:
                    severity_increases += 1
                elif calculated_idx < existing_idx:
                    severity_decreases += 1
        
        print(f"  Risk increases: {severity_increases} EGIDs")
        print(f"  Risk decreases: {severity_decreases} EGIDs")
        print(f"  Same level (different labels): {len(self.mismatches_df) - severity_increases - severity_decreases} EGIDs")
    
    def export_results(self):
        """Export results to Excel files"""
        print("\n" + "="*70)
        print("EXPORTING RESULTS")
        print("="*70)
        
        # Export complete analysis
        output_file = os.path.join(config.RESULTS_DIR, config.OUTPUT_FILES['complete_analysis'])
        self.results_df.to_excel(output_file, index=False)
        print(f"\n✓ Complete analysis exported to: {output_file}")
        
        # Export mismatches
        if len(self.mismatches_df) > 0:
            mismatch_file = os.path.join(config.RESULTS_DIR, config.OUTPUT_FILES['mismatches'])
            self.mismatches_df.to_excel(mismatch_file, index=False)
            print(f"✓ Mismatches exported to: {mismatch_file}")
        
        # Export summary report
        self._export_summary_report()
        
        print("\n✓ All exports completed successfully!")
    
    def _export_summary_report(self):
        """Export text summary report"""
        report_file = os.path.join(config.RESULTS_DIR, config.OUTPUT_FILES['summary_report'])
        
        with open(report_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("ISRR ANALYSIS SUMMARY REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Total EGIDs Processed: {len(self.results_df)}\n")
            f.write(f"Total Mismatches: {len(self.mismatches_df)}\n")
            
            match_rate = ((len(self.results_df) - len(self.mismatches_df)) / len(self.results_df) * 100) if len(self.results_df) > 0 else 0
            f.write(f"Match Rate: {match_rate:.1f}%\n\n")
            
            f.write("ISRR Distribution:\n")
            for isrr_level in ['Minor', 'Low', 'Moderate', 'High', 'Critical']:
                count = len(self.results_df[self.results_df['Calculated_Final_ISRR'] == isrr_level])
                percentage = (count / len(self.results_df) * 100) if len(self.results_df) > 0 else 0
                f.write(f"  {isrr_level}: {count} ({percentage:.1f}%)\n")
            
            f.write("\nInterim to Final Changes:\n")
            changes = len(self.results_df[self.results_df['Interim_to_Final_Change'] == 'Yes'])
            f.write(f"  Total changes: {changes}\n")
            
        print(f"✓ Summary report exported to: {report_file}")
    
    def print_sample_results(self, num_samples=None):
        """Print sample comparison results"""
        if num_samples is None:
            num_samples = config.MAX_SAMPLE_DISPLAY
        
        print("\n" + "="*70)
        print(f"SAMPLE COMPARISON RESULTS (First {num_samples} EGIDs)")
        print("="*70)
        
        for i, row in self.results_df.head(num_samples).iterrows():
            print(f"\nEGID: {row['EGID']}")
            print(f"  Existing ISRR: {row['Existing_ISRR_Value']}")
            print(f"  Calculated Interim: {row['Calculated_Interim_ISRR']}")
            print(f"  Calculated Final: {row['Calculated_Final_ISRR']}")
            print(f"  Match: {row['ISRR_Match']}")
            print(f"  Modifier: {row['Modifier_Applied']}")