"""
Interim ISRR Calculator Module
Calculates interim ISRR based on data characteristics and business rules
"""

from collections import defaultdict
import config

class InterimISRRCalculator:
    """
    Calculates interim ISRR for each EGID based on data group combinations
    """
    
    def __init__(self, variables_df, interimisrr_df):
        self.variables_df = variables_df
        self.interimisrr_df = interimisrr_df
        self.interim_results = {}
        
    def determine_data_groups_and_nature(self, egid_analysis_data):
        """Determine data group combinations and nature of data"""
        groups = egid_analysis_data['groups']
        
        transactional_groups = set()
        non_transactional_groups = set()
        
        for group_name, variables in groups.items():
            has_transactional = False
            for var in variables:
                var_info = self.variables_df[
                    self.variables_df[config.VARIABLES_COLUMNS['name']] == var
                ]
                if not var_info.empty and var_info.iloc[0][config.VARIABLES_COLUMNS['type']] == 'transactional':
                    has_transactional = True
                    break
            
            if has_transactional:
                transactional_groups.add(group_name)
            else:
                non_transactional_groups.add(group_name)
        
        num_transactional = len(transactional_groups)
        num_non_transactional = len(non_transactional_groups)
        
        # Apply business rules
        if num_transactional == 0 and num_non_transactional == 1:
            nature = "1 Data group without Transactional Data – No impact to clients and/or staff or continuity of business due to data breach"
        elif num_transactional == 1 or (num_transactional == 0 and num_non_transactional == 2):
            nature = "1 Transactional Data group OR Combination of 2 Data group without Transactional Data"
        elif (num_transactional == 0 and num_non_transactional > 2) or (num_transactional == 1 and num_non_transactional >= 2) or (num_transactional == 2):
            nature = "Combination of > 2 Data group without Transactional Data OR Combination of ≥ 2 with 1 Transactional Data group OR Combination of 2 Transactional Data groups"
        elif num_transactional == 2 and num_non_transactional >= 2:
            nature = "Combination of ≥ 2 Data group with 2 Transactional Data groups"
        elif num_transactional >= 3 and num_non_transactional >= 2:
            nature = "Combination of ≥ 2 Data group with 3 Transactional Data groups"
        else:
            nature = "Other combination"
        
        return {
            'nature_of_data': nature,
            'transactional_groups': list(transactional_groups),
            'non_transactional_groups': list(non_transactional_groups),
            'num_transactional': num_transactional,
            'num_non_transactional': num_non_transactional
        }
    
    def get_bank_data_classification(self, egid_analysis_data):
        """Determine bank data classification (D2, D3, D4)"""
        categories = egid_analysis_data['categories']
        
        # Check D4 (highest risk)
        d4_categories = config.BANK_DATA_RULES['D4']
        if all(cat in categories for cat in d4_categories):
            return 'D4'
        
        # Check D3
        d3_categories = config.BANK_DATA_RULES['D3']
        if any(cat in categories for cat in d3_categories):
            return 'D3'
        
        # Check D2
        d2_categories = config.BANK_DATA_RULES['D2']
        if any(cat in categories for cat in d2_categories):
            return 'D2'
        
        return 'Not considered'
    
    def get_highest_classification(self, egid_analysis_data):
        """Get the highest security classification"""
        classifications = egid_analysis_data['classifications']
        
        for classification in config.CLASSIFICATION_HIERARCHY:
            if classification.lower() in [c.lower() for c in classifications]:
                return classification
        
        return 'Internal / Confidential'
    
    def get_availability_requirement(self, egid_analysis_data):
        """Determine availability requirement based on data criticality"""
        transactional_count = len(egid_analysis_data.get('transactional_groups', []))
        
        if transactional_count >= 3:
            return 'Not considered'
        elif transactional_count >= 2:
            return 'High Availability (Less than 10% downtime or non-availability of hard copy data for 3 days)'
        elif transactional_count >= 1:
            return 'Medium Availability (Less than 25% downtime or non-availability of hard copy data for 8 days)'
        else:
            return 'Very Low Availability (Downtime or non-availability of data does not have an impact)'
    
    def calculate_interim_isrr(self, egid, egid_analysis_data):
        """Calculate interim ISRR for a given EGID"""
        data_nature_info = self.determine_data_groups_and_nature(egid_analysis_data)
        nature_of_data = data_nature_info['nature_of_data']
        bank_data = self.get_bank_data_classification(egid_analysis_data)
        highest_classification = self.get_highest_classification(egid_analysis_data)
        availability = self.get_availability_requirement(egid_analysis_data)
        
        # Try to match with interim ISRR rules
        for idx, rule in self.interimisrr_df.iterrows():
            rule_nature = rule[config.INTERIM_ISRR_COLUMNS['nature_of_data']]
            rule_bank_data = rule[config.INTERIM_ISRR_COLUMNS['bank_data']]
            rule_classification = rule[config.INTERIM_ISRR_COLUMNS['highest_classification']]
            rule_availability = rule[config.INTERIM_ISRR_COLUMNS['availability']]
            rule_isrr = rule[config.INTERIM_ISRR_COLUMNS['interim_isrr']]
            
            # Check if current data matches this rule
            nature_match = (rule_nature == nature_of_data or rule_nature == "Not considered")
            bank_data_match = (rule_bank_data == bank_data or rule_bank_data == "Not considered")
            classification_match = (rule_classification == highest_classification or rule_classification == "Not considered")
            availability_match = (rule_availability == availability or rule_availability == "Not considered")
            
            if nature_match and bank_data_match and classification_match and availability_match:
                return {
                    'interim_isrr': rule_isrr,
                    'nature_of_data': nature_of_data,
                    'bank_data': bank_data,
                    'highest_classification': highest_classification,
                    'availability': availability,
                    'matched_rule': f"Rule {idx+1}",
                    'data_groups_info': data_nature_info
                }
        
        # Fallback logic if no rule matches
        default_isrr = self._get_default_isrr(nature_of_data)
        
        return {
            'interim_isrr': default_isrr,
            'nature_of_data': nature_of_data,
            'bank_data': bank_data,
            'highest_classification': highest_classification,
            'availability': availability,
            'matched_rule': "Default rule applied",
            'data_groups_info': data_nature_info
        }
    
    def _get_default_isrr(self, nature_of_data):
        """Get default ISRR based on nature of data"""
        if "Critical" in nature_of_data or "3 Transactional" in nature_of_data:
            return "Critical"
        elif "High" in nature_of_data or "2 Transactional" in nature_of_data:
            return "High"
        elif "Moderate" in nature_of_data or "1 Transactional" in nature_of_data:
            return "Moderate"
        elif "Low" in nature_of_data:
            return "Low"
        else:
            return "Minor"
    
    def calculate_all(self, egid_analysis):
        """Calculate interim ISRR for all EGIDs"""
        print("\n" + "="*70)
        print("STEP 2: INTERIM ISRR CALCULATION")
        print("="*70)
        
        egids = list(egid_analysis.keys())
        print(f"\nCalculating interim ISRR for {len(egids)} EGIDs...")
        
        for i, egid in enumerate(egids):
            if i % config.PROGRESS_INTERVAL == 0:
                print(f"Processing EGID {i+1}/{len(egids)}: {egid}")
            
            egid_data = egid_analysis[egid]
            interim_result = self.calculate_interim_isrr(egid, egid_data)
            self.interim_results[egid] = interim_result
        
        print(f"\n✓ Completed interim ISRR calculation for all {len(egids)} EGIDs")
        self._print_distribution()
        
        return self.interim_results
    
    def _print_distribution(self):
        """Print distribution of interim ISRR values"""
        print("\n" + "="*70)
        print("INTERIM ISRR DISTRIBUTION")
        print("="*70)
        
        distribution = defaultdict(int)
        for result in self.interim_results.values():
            distribution[result['interim_isrr']] += 1
        
        total = len(self.interim_results)
        for isrr_level in ['Minor', 'Low', 'Moderate', 'High', 'Critical']:
            count = distribution.get(isrr_level, 0)
            percentage = (count / total * 100) if total > 0 else 0
            print(f"{isrr_level}: {count} EGIDs ({percentage:.1f}%)")
    
    def print_sample_results(self, num_samples=None):
        """Print sample results for verification"""
        if num_samples is None:
            num_samples = config.MAX_SAMPLE_DISPLAY
        
        print("\n" + "="*70)
        print(f"SAMPLE INTERIM ISRR RESULTS (First {num_samples} EGIDs)")
        print("="*70)
        
        for i, (egid, result) in enumerate(list(self.interim_results.items())[:num_samples]):
            print(f"\nEGID: {egid}")
            print(f"  Interim ISRR: {result['interim_isrr']}")
            print(f"  Nature of Data: {result['nature_of_data']}")
            print(f"  Bank Data: {result['bank_data']}")
            print(f"  Highest Classification: {result['highest_classification']}")
            print(f"  Data Groups: {result['data_groups_info']['num_transactional']} transactional, {result['data_groups_info']['num_non_transactional']} non-transactional")