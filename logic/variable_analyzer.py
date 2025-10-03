"""
Variable Analyzer Module
Handles variable grouping and classification for each EGID
"""

from collections import defaultdict
import config

class VariableAnalyzer:
    """
    Analyzes and groups variables for each EGID based on TRUE/FALSE values
    """
    
    def __init__(self, variables_df, rfimapped_df, egid_column):
        self.variables_df = variables_df
        self.rfimapped_df = rfimapped_df
        self.egid_column = egid_column
        self.egid_analysis = {}
        
    def analyze_all_egids(self):
        """Analyze variables for all EGIDs"""
        print("\n" + "="*70)
        print("STEP 1: VARIABLE GROUPING & CLASSIFICATION")
        print("="*70)
        
        egids = self.rfimapped_df[self.egid_column].unique()
        print(f"\nProcessing {len(egids)} unique EGIDs...")
        print(f"Sample EGIDs: {list(egids[:3])}")
        
        for i, egid in enumerate(egids):
            if i % config.PROGRESS_INTERVAL == 0:
                print(f"Processing EGID {i+1}/{len(egids)}: {egid}")
            
            # Get the row for this EGID
            egid_row = self.rfimapped_df[self.rfimapped_df[self.egid_column] == egid].iloc[0]
            
            # Initialize containers for this EGID
            egid_groups = defaultdict(list)
            egid_types = defaultdict(list)
            egid_categories = defaultdict(list)
            egid_classifications = defaultdict(list)
            
            # Check each variable
            for _, var_row in self.variables_df.iterrows():
                var_name = var_row[config.VARIABLES_COLUMNS['name']]
                var_group = var_row[config.VARIABLES_COLUMNS['group']]
                var_type = var_row[config.VARIABLES_COLUMNS['type']]
                var_category = var_row[config.VARIABLES_COLUMNS['category']]
                var_classification = var_row[config.VARIABLES_COLUMNS['classification']]
                
                # Check if this variable column exists in rfimapped and if it's TRUE
                if var_name in self.rfimapped_df.columns:
                    if egid_row[var_name] == True:
                        egid_groups[var_group].append(var_name)
                        egid_types[var_type].append(var_name)
                        egid_categories[var_category].append(var_name)
                        egid_classifications[var_classification].append(var_name)
            
            # Store analysis for this EGID
            self.egid_analysis[egid] = {
                'groups': dict(egid_groups),
                'types': dict(egid_types),
                'categories': dict(egid_categories),
                'classifications': dict(egid_classifications)
            }
        
        print(f"\n✓ Completed processing all {len(egids)} EGIDs")
        self._print_summary_statistics()
        
        return self.egid_analysis
    
    def _print_summary_statistics(self):
        """Print summary statistics of variable analysis"""
        print("\n" + "="*70)
        print("VARIABLE ANALYSIS SUMMARY")
        print("="*70)
        
        # Count variables by group across all EGIDs
        group_counts = defaultdict(int)
        type_counts = defaultdict(int)
        category_counts = defaultdict(int)
        
        for egid, analysis in self.egid_analysis.items():
            for group, vars_list in analysis['groups'].items():
                group_counts[group] += len(vars_list)
            for type_name, vars_list in analysis['types'].items():
                type_counts[type_name] += len(vars_list)
            for category, vars_list in analysis['categories'].items():
                category_counts[category] += len(vars_list)
        
        print("\nVariable Group Distribution:")
        for group, count in sorted(group_counts.items()):
            print(f"  {group}: {count} occurrences")
        
        print("\nVariable Type Distribution:")
        for type_name, count in sorted(type_counts.items()):
            print(f"  {type_name}: {count} occurrences")
        
        print("\nVariable Category Distribution:")
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count} occurrences")
    
    def get_egid_analysis(self, egid):
        """Get analysis results for a specific EGID"""
        return self.egid_analysis.get(egid, None)
    
    def print_sample_results(self, num_samples=None):
        """Print sample results for verification"""
        if num_samples is None:
            num_samples = config.MAX_SAMPLE_DISPLAY
            
        print("\n" + "="*70)
        print(f"SAMPLE RESULTS (First {num_samples} EGIDs)")
        print("="*70)
        
        for i, (egid, analysis) in enumerate(list(self.egid_analysis.items())[:num_samples]):
            print(f"\nEGID: {egid}")
            print(f"  Groups with TRUE variables:")
            for group, vars_list in analysis['groups'].items():
                print(f"    {group}: {len(vars_list)} variables - {vars_list[:3]}{'...' if len(vars_list) > 3 else ''}")
            
            print(f"  Types:")
            for type_name, vars_list in analysis['types'].items():
                print(f"    {type_name}: {len(vars_list)} variables")
