"""
Main execution script for ISRR Analysis
Run this file to execute the complete analysis workflow
"""

import sys
import time
from datetime import datetime

# Import all modules from logic package
from logic.data_loader import DataLoader
from logic.variable_analyzer import VariableAnalyzer
from logic.interim_isrr_calculator import InterimISRRCalculator
from logic.final_isrr_calculator import FinalISRRCalculator
from logic.comparator import ISRRComparator

def print_header():
    """Print application header"""
    print("\n" + "="*70)
    print(" " * 15 + "ISRR ANALYSIS SYSTEM")
    print(" " * 10 + "Inherent Security Risk Rating Calculator")
    print("="*70)
    print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")

def print_footer(start_time):
    """Print application footer with execution time"""
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"Execution completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total execution time: {minutes}m {seconds}s")
    print("="*70 + "\n")

def main():
    """Main execution function"""
    start_time = time.time()
    
    try:
        print_header()
        
        # ====================================================================
        # PHASE 1: DATA LOADING AND PREPARATION
        # ====================================================================
        print("📥 PHASE 1: DATA LOADING AND PREPARATION")
        print("-" * 70)
        
        loader = DataLoader()
        loader.load_all_files()
        loader.identify_egid_column()
        loader.clean_rfimapped_data()
        loader.clean_mainrfi_data()
        loader.print_summary()
        
        # ====================================================================
        # PHASE 2: VARIABLE ANALYSIS
        # ====================================================================
        print("\n\n🔍 PHASE 2: VARIABLE GROUPING & CLASSIFICATION")
        print("-" * 70)
        
        analyzer = VariableAnalyzer(
            loader.variables_df,
            loader.rfimapped_df,
            loader.egid_column
        )
        egid_analysis = analyzer.analyze_all_egids()
        analyzer.print_sample_results()
        
        # ====================================================================
        # PHASE 3: INTERIM ISRR CALCULATION
        # ====================================================================
        print("\n\n📊 PHASE 3: INTERIM ISRR CALCULATION")
        print("-" * 70)
        
        interim_calculator = InterimISRRCalculator(
            loader.variables_df,
            loader.interimisrr_df
        )
        interim_results = interim_calculator.calculate_all(egid_analysis)
        interim_calculator.print_sample_results()
        
        # ====================================================================
        # PHASE 4: FINAL ISRR CALCULATION
        # ====================================================================
        print("\n\n🎯 PHASE 4: FINAL ISRR CALCULATION (OR LOGIC)")
        print("-" * 70)
        
        final_calculator = FinalISRRCalculator(
            loader.mainrfi_df,
            loader.finalisrr_df,
            loader.egid_column
        )
        final_results = final_calculator.calculate_all(interim_results)
        
        # ====================================================================
        # PHASE 5: COMPARISON AND REPORTING
        # ====================================================================
        print("\n\n🔄 PHASE 5: COMPARISON WITH EXISTING VALUES")
        print("-" * 70)
        
        comparator = ISRRComparator(
            loader.mainrfi_df,
            loader.egid_column
        )
        results_df, mismatches_df = comparator.compare_results(
            egid_analysis,
            interim_results,
            final_results
        )
        comparator.print_sample_results()
        
        # ====================================================================
        # PHASE 6: EXPORT RESULTS
        # ====================================================================
        print("\n\n💾 PHASE 6: EXPORTING RESULTS")
        print("-" * 70)
        
        comparator.export_results()
        
        # ====================================================================
        # FINAL SUMMARY
        # ====================================================================
        print("\n\n📈 FINAL SUMMARY")
        print("="*70)
        print(f"✓ Total EGIDs Processed: {len(results_df)}")
        print(f"✓ Variables Analyzed: {len(loader.variables_df)}")
        print(f"✓ Interim ISRR Calculated: {len(interim_results)}")
        print(f"✓ Final ISRR Calculated: {len(final_results)}")
        print(f"✓ Mismatches Identified: {len(mismatches_df)}")
        
        match_rate = ((len(results_df) - len(mismatches_df)) / len(results_df) * 100) if len(results_df) > 0 else 0
        print(f"✓ Overall Match Rate: {match_rate:.1f}%")
        
        print("\n📁 OUTPUT FILES GENERATED:")
        print(f"  • Complete Analysis: complete_isrr_analysis.xlsx")
        if len(mismatches_df) > 0:
            print(f"  • Mismatches Report: isrr_mismatches.xlsx")
        print(f"  • Summary Report: isrr_summary_report.txt")
        
        print_footer(start_time)
        
        print("✅ SUCCESS: ISRR Analysis completed successfully!")
        print("You can now review the exported files and dashboard.\n")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: Required file not found - {e}")
        print("Please ensure all input files are in the correct location.")
        return 1
        
    except KeyError as e:
        print(f"\n❌ ERROR: Column not found in data - {e}")
        print("Please verify column names in config.py match your Excel files.")
        return 1
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    print("\n" + "🚀 Starting ISRR Analysis System...")
    exit_code = main()
    
    if exit_code == 0:
        print("="*70)
        print("📊 To view the interactive dashboard, run:")
        print("   streamlit run dashboard.py")
        print("="*70)
    
    sys.exit(exit_code)