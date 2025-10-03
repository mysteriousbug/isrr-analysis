"""
Final ISRR Calculator Module
Calculates final ISRR with operational modifiers using OR logic
"""

from collections import defaultdict
import pandas as pd
import config

class FinalISRRCalculator:
    """
    Calculates final ISRR based on interim ISRR and operational factors
    """
    
    def __init__(self, mainrfi_df, finalisrr_df, egid_column):
        self.mainrfi_df = mainrfi_df
        self.finalisrr_df = finalisrr_df
        self.egid_column = egid_column
        self.final_results = {}
        
    def clean_volume_data(self, volume_str):
        """Clean and standardize volume data"""
        if pd.isna(volume_str) or str(volume_str).strip() == '':
            return 'Not considered'
        
        volume_str = str(volume_str).strip()
        
        # Check predefined mappings
        for key, value in config.VOLUME_MAPPINGS.items():
            if key in volume_str:
                return value
        
        return 'Not considered'
    
    def clean_format_data(self, format_str):
        """Clean and standardize format data"""
        if pd.isna(format_str) or str(format_str).strip() == '':
            return 'Not considered'
        
        format_str = str(format_str).strip().lower()
        
        for key, value in config.FORMAT_MAPPINGS.items():
            if key in format_str:
                return value
        
        return 'Not considered'
    
    def clean_connectivity_data(self, connectivity_str):
        """Clean and standardize connectivity data"""
        if pd.isna(connectivity_str) or str(connectivity_str).strip() == '' or '#ERROR!' in str(connectivity_str):
            return 'Not considered'
        
        connectivity_str = str(connectivity_str).strip().lower()
        
        for key, value in config.CONNECTIVITY_MAPPINGS.items():
            if key in connectivity_str:
                return value
        
        return 'Not considered'
    
    def get_mainrfi_data_for_egid(self, egid):
        """Get main RFI data for a specific EGID"""
        mainrfi_row = None
        
        for col in config.EGID_COLUMN_VARIATIONS:
            if col in self.mainrfi_df.columns:
                matching_rows = self.mainrfi_df[self.mainrfi_df[col] == egid]
                if not matching_rows.empty:
                    mainrfi_row = matching_rows.iloc[0]
                    break
        
        if mainrfi_row is None:
            return {
                'volume': 'Not considered',
                'format': 'Not considered',
                'connectivity': 'Not considered'
            }
        
        volume = self.clean_volume_data(mainrfi_row.get(config.MAINRFI_COLUMNS['volume'], 'Not considered'))
        format_data = self.clean_format_data(mainrfi_row.get(config.MAINRFI_COLUMNS['format'], 'Not considered'))
        connectivity = self.clean_connectivity_data(mainrfi_row.get(config.MAINRFI_COLUMNS['connectivity'], 'Not considered'))
        
        return {
            'volume': volume,
            'format': format_data,
            'connectivity': connectivity
        }
    
    def map_interim_to_modifier_base(self, interim_isrr):
        """Map interim ISRR to base value for modifier calculations"""
        return config.ISRR_TO_NUMBER.get(interim_isrr, 3)
    
    def number_to_isrr(self, number):
        """Convert number back to ISRR level"""
        if number < 1:
            number = 1
        elif number > 5:
            number = 5
        return config.NUMBER_TO_ISRR[number]
    
    def calculate_final_isrr(self, egid, interim_isrr):
        """Calculate final ISRR based on interim ISRR and final ISRR rules using OR logic"""
        mainrfi_data = self.get_mainrfi_data_for_egid(egid)
        
        volume = mainrfi_data['volume']
        format_data = mainrfi_data['format']
        connectivity = mainrfi_data['connectivity']
        
        base_isrr_number = self.map_interim_to_modifier_base(interim_isrr)
        
        matching_rules = []
        
        for idx, rule in self.finalisrr_df.iterrows():
            rule_modifier = rule[config.FINAL_ISRR_COLUMNS['modifier']]
            rule_volume = rule[config.FINAL_ISRR_COLUMNS['volume']]
            rule_format = rule[config.FINAL_ISRR_COLUMNS['format']]
            rule_connectivity = rule[config.FINAL_ISRR_COLUMNS['connectivity']]
            rule_final_isrr = rule[config.FINAL_ISRR_COLUMNS['final_isrr']]
            
            # Check each condition independently (OR logic)
            volume_triggers = False
            format_triggers = False
            connectivity_triggers = False
            
            if rule_volume != 'Not considered':
                if volume == rule_volume:
                    volume_triggers = True
                elif '<' in str(rule_volume) and '<' in str(volume):
                    try:
                        rule_num = int(str(rule_volume).replace('<', ''))
                        volume_num = int(str(volume).replace('<', ''))
                        if volume_num <= rule_num:
                            volume_triggers = True
                    except:
                        pass
            
            if rule_format != 'Not considered':
                if format_data == rule_format:
                    format_triggers = True
            
            if rule_connectivity != 'Not considered':
                if connectivity == rule_connectivity:
                    connectivity_triggers = True
            
            # OR Logic: Rule applies if ANY condition is met
            rule_applies = volume_triggers or format_triggers or connectivity_triggers
            
            # Also apply universal rules
            if (rule_volume == 'Not considered' and 
                rule_format == 'Not considered' and 
                rule_connectivity == 'Not considered'):
                rule_applies = True
            
            if rule_applies:
                matching_rules.append({
                    'rule': rule,
                    'modifier': rule_modifier,
                    'final_isrr': rule_final_isrr,
                    'volume_triggered': volume_triggers,
                    'format_triggered': format_triggers,
                    'connectivity_triggered': connectivity_triggers,
                    'conditions_met': [
                        'Volume' if volume_triggers else None,
                        'Format' if format_triggers else None,
                        'Connectivity' if connectivity_triggers else None
                    ],
                    'rule_volume': rule_volume,
                    'rule_format': rule_format,
                    'rule_connectivity': rule_connectivity
                })
        
        if matching_rules:
            # Prioritize rules
            def rule_priority(rule_data):
                specificity = sum([
                    1 if rule_data['rule_volume'] != 'Not considered' else 0,
                    1 if rule_data['rule_format'] != 'Not considered' else 0,
                    1 if rule_data['rule_connectivity'] != 'Not considered' else 0
                ])
                
                risk_impact = config.RISK_LEVEL_PRIORITY.get(rule_data['final_isrr'], 3)
                has_modifier = 1 if 'ISRR' in rule_data['modifier'] else 0
                
                return (specificity, risk_impact, has_modifier)
            
            best_rule = max(matching_rules, key=rule_priority)
            
            # Apply the modifier
            modifier = best_rule['modifier']
            if 'ISRR + 1' in modifier:
                adjusted_number = base_isrr_number + 1
                final_isrr = self.number_to_isrr(adjusted_number)
            elif 'ISRR - 1' in modifier:
                adjusted_number = base_isrr_number - 1
                final_isrr = self.number_to_isrr(adjusted_number)
            else:
                final_isrr = best_rule['final_isrr']
            
            conditions_met = [c for c in best_rule['conditions_met'] if c is not None]
            
            return {
                'final_isrr': final_isrr,
                'interim_isrr': interim_isrr,
                'modifier_applied': modifier,
                'volume': volume,
                'format': format_data,
                'connectivity': connectivity,
                'matched_rule': f"OR Logic - Conditions met: {', '.join(conditions_met) if conditions_met else 'Universal rule'}",
                'rule_details': best_rule,
                'total_matching_rules': len(matching_rules),
                'or_logic_applied': True
            }
        else:
            return {
                'final_isrr': interim_isrr,
                'interim_isrr': interim_isrr,
                'modifier_applied': 'None - No matching rule',
                'volume': volume,
                'format': format_data,
                'connectivity': connectivity,
                'matched_rule': 'No match - using interim ISRR',
                'rule_details': None,
                'total_matching_rules': 0,
                'or_logic_applied': False
            }
    
    def calculate_all(self, interim_results):
        """Calculate final ISRR for all EGIDs"""
        print("\n" + "="*70)
        print("STEP 3: FINAL ISRR CALCULATION (OR LOGIC)")
        print("="*70)
        
        egids = list(interim_results.keys())
        print(f"\nCalculating final ISRR for {len(egids)} EGIDs...")
        
        for i, egid in enumerate(egids):
            if i % config.PROGRESS_INTERVAL == 0:
                print(f"Processing EGID {i+1}/{len(egids)}: {egid}")
            
            interim_result = interim_results[egid]
            interim_isrr = interim_result['interim_isrr']
            
            final_result = self.calculate_final_isrr(egid, interim_isrr)
            self.final_results[egid] = final_result
        
        print(f"\n✓ Completed final ISRR calculation for all {len(egids)} EGIDs")
        self._print_distribution()
        
        return self.final_results
    
    def _print_distribution(self):
        """Print distribution of final ISRR values"""
        print("\n" + "="*70)
        print("FINAL ISRR DISTRIBUTION")
        print("="*70)
        
        distribution = defaultdict(int)
        modifier_distribution = defaultdict(int)
        
        for result in self.final_results.values():
            distribution[result['final_isrr']] += 1
            modifier_distribution[result['modifier_applied']] += 1
        
        total = len(self.final_results)
        
        print("\nFinal ISRR Levels:")
        for isrr_level in ['Minor', 'Low', 'Moderate', 'High', 'Critical']:
            count = distribution.get(isrr_level, 0)
            percentage = (count / total * 100) if total > 0 else 0
            print(f"  {isrr_level}: {count} EGIDs ({percentage:.1f}%)")
        
        print("\nTop Modifiers Applied:")
        for modifier, count in sorted(modifier_distribution.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {modifier}: {count} EGIDs")