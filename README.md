# ISRR Analysis System

**Inherent Security Risk Rating Calculator with Interactive Dashboard**

A comprehensive Python-based system for calculating and validating Inherent Security Risk Ratings (ISRR) for bank engagement IDs, featuring an interactive Streamlit dashboard.

---

## 📁 Project Structure

```
isrr-analysis/
│
├── run.py                          # Main execution script (START HERE)
├── dashboard.py                    # Streamlit interactive dashboard
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── data/                           # Input data files
│   ├── variables.xlsx
│   ├── rfimapped.xlsx
│   ├── mainrfi.xlsx
│   ├── interimisrr.xlsx
│   └── finalisrr.xlsx
│
├── logic/                          # Business logic modules
│   ├── __init__.py
│   ├── config.py                   # Configuration and constants
│   ├── data_loader.py              # Data loading and cleaning
│   ├── variable_analyzer.py        # Variable grouping logic
│   ├── interim_isrr_calculator.py  # Interim ISRR calculation
│   ├── final_isrr_calculator.py    # Final ISRR calculation (OR logic)
│   └── comparator.py               # Results comparison and export
│
├── utils/                          # Utility scripts
│   └── egid_diagnostic.py          # Diagnostic tool for troubleshooting
│
└── results/                        # Output files (auto-generated)
    ├── complete_isrr_analysis.xlsx
    ├── isrr_mismatches.xlsx
    └── isrr_summary_report.txt
```

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Step 1: Run the Analysis

```bash
python run.py
```

### Step 2: Launch the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## 📊 Streamlit Dashboard Features

### **Interactive & Dynamic**
✨ **Real-time Filtering** - Filter by ISRR level, match status  
📈 **Live Charts** - Interactive Plotly visualizations  
🔍 **Search Functionality** - Search any EGID or data  
💾 **Dynamic Export** - Download filtered results on-demand  
🎨 **Beautiful UI** - Modern, professional design  

### **Dashboard Tabs**

1. **📈 Overview**
   - ISRR distribution comparison (Existing vs Calculated)
   - Risk change analysis (Interim → Final)
   - Data groups scatter plot
   - Key statistics and metrics

2. **⚠️ Mismatches**
   - Detailed mismatch analysis
   - Severity analysis (increases/decreases)
   - Top mismatch patterns
   - Searchable mismatch table
   - Export filtered mismatches

3. **🔄 Flow Analysis**
   - Interactive Sankey diagram (Interim → Final flow)
   - Modifier application analysis
   - Visual flow of risk calculations

4. **📋 Data Table**
   - Complete analysis results
   - Column selection
   - Search across all fields
   - Sortable and filterable

5. **💾 Export**
   - Download complete analysis (CSV/Excel)
   - Download mismatches
   - Generate summary reports
   - Custom filtered exports

### **Sidebar Controls**
- **ISRR Level Filter**: Select specific risk levels
- **Match Status Filter**: View all, matched, or mismatched only
- **Dynamic Metrics**: Update based on filters

---

## 📊 Analysis Workflow

### **Phase 1: Data Loading**
- Loads 5 Excel input files from `data/` folder
- Identifies EGID column automatically
- Cleans and standardizes data
- Removes duplicates and null values

### **Phase 2: Variable Grouping**
- For each EGID, identifies TRUE variables
- Groups by: group, type, category, classification
- Distinguishes transactional vs non-transactional

### **Phase 3: Interim ISRR Calculation**
- Determines nature of data combinations
- Applies bank data classification (D2/D3/D4)
- Evaluates highest classification level
- Matches against interim ISRR rules
- Outputs: Minor/Low/Moderate/High/Critical

### **Phase 4: Final ISRR Calculation**
- Extracts volume, format, connectivity from mainrfi
- Applies **OR logic** rule matching
- Applies modifiers (ISRR +1, ISRR -1)
- Prioritizes most specific rules
- Outputs: Adjusted final ISRR

### **Phase 5: Comparison**
- Compares calculated vs existing ISRR
- Identifies mismatches
- Analyzes severity (increases/decreases)
- Generates detailed reports in `results/` folder

---

## 🔧 Configuration

Edit `logic/config.py` to customize:

### File Paths
```python
INPUT_FILES = {
    'variables': os.path.join('data', 'variables.xlsx'),
    'rfimapped': os.path.join('data', 'rfimapped.xlsx'),
    ...
}

OUTPUT_FILES = {
    'complete_analysis': 'complete_isrr_analysis.xlsx',
    'mismatches': 'isrr_mismatches.xlsx',
    ...
}
```

### Column Mappings
```python
MAINRFI_COLUMNS = {
    'volume': 'Tpmaxrecordscanprocess',
    'format': 'Isdataelecform',
    ...
}
```

### Business Rules
```python
BANK_DATA_RULES = {
    'D4': ['personal_identifiable_information', 'employee_data'],
    'D3': ['transactional_data'],
    ...
}
```

---

## 📖 Module Details

### `logic/config.py`
**Purpose:** Centralized configuration  
**Contains:** File paths, column mappings, business rules, constants

### `logic/data_loader.py`
**Purpose:** Load and clean input data  
**Key Functions:**
- `load_all_files()` - Loads 5 Excel files from `data/` folder
- `identify_egid_column()` - Auto-detects EGID column
- `clean_rfimapped_data()` - Removes duplicates, nulls, whitespace
- `clean_mainrfi_data()` - Standardizes EGID columns

### `logic/variable_analyzer.py`
**Purpose:** Group and classify variables  
**Key Functions:**
- `analyze_all_egids()` - Process all EGIDs
- Returns: Dictionary of grouped variables per EGID

### `logic/interim_isrr_calculator.py`
**Purpose:** Calculate interim ISRR  
**Key Functions:**
- `determine_data_groups_and_nature()` - Counts transactional/non-transactional groups
- `get_bank_data_classification()` - Returns D2/D3/D4
- `calculate_interim_isrr()` - Matches rules, returns interim ISRR

### `logic/final_isrr_calculator.py`
**Purpose:** Calculate final ISRR with OR logic  
**Key Functions:**
- `clean_volume_data()` - Standardizes volume values
- `get_mainrfi_data_for_egid()` - Extracts operational data
- `calculate_final_isrr()` - Applies OR logic and modifiers

**OR Logic Implementation:**
- Rule triggers if **ANY** condition matches (Volume OR Format OR Connectivity)
- Prioritizes: Specificity > Risk Impact > Modifier Presence

### `logic/comparator.py`
**Purpose:** Compare and export results  
**Key Functions:**
- `compare_results()` - Compares calculated vs existing ISRR
- `export_results()` - Exports to `results/` folder
- `_analyze_mismatch_severity()` - Analyzes risk increases/decreases

### `utils/egid_diagnostic.py`
**Purpose:** Troubleshooting tool  
**Use When:** EGIDs are missing from output  
**Run:** `python utils/egid_diagnostic.py`

### `dashboard.py`
**Purpose:** Interactive Streamlit dashboard  
**Features:**
- Real-time data visualization with Plotly
- Interactive filters and search
- Dynamic exports
- Multiple analysis views
- Professional UI/UX

---

## 📤 Output Files (in `results/` folder)

### `complete_isrr_analysis.xlsx`
Complete analysis with columns:
- EGID
- Existing_ISRR_Value
- Calculated_Interim_ISRR
- Calculated_Final_ISRR
- ISRR_Match (Yes/No)
- Nature_of_Data
- Bank_Data (D2/D3/D4)
- Volume, Format, Connectivity
- Modifier_Applied
- Transactional/Non-Transactional group counts
- Rule matching details

### `isrr_mismatches.xlsx`
Only mismatched EGIDs:
- EGID
- Existing_ISRR
- Calculated_Final_ISRR
- Difference (e.g., "Low → Moderate")

### `isrr_summary_report.txt`
Text summary:
- Total EGIDs processed
- Match rate
- ISRR distribution
- Change statistics

---

## 🐛 Troubleshooting

### Issue: "EGIDs missing from output"
**Solution:** Run diagnostic script
```bash
python utils/egid_diagnostic.py
```
This will identify:
- Column name issues
- Data type mismatches
- Whitespace problems
- Duplicate EGIDs

### Issue: "Column not found"
**Solution:** Update column names in `logic/config.py`
- Check your Excel files for exact column names
- Update `MAINRFI_COLUMNS`, `VARIABLES_COLUMNS`, etc.

### Issue: "FileNotFoundError"
**Solution:** Ensure all input files are in the `data/` folder

### Issue: "Wrong ISRR calculations"
**Solution:** Verify business rules in `logic/config.py`
- Check `BANK_DATA_RULES`
- Verify volume/format/connectivity mappings
- Review nature of data logic

### Issue: "Dashboard not loading data"
**Solution:** Run the analysis first
```bash
python run.py
```
The dashboard needs results files in the `results/` folder

### Issue: "Streamlit not found"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🎨 Dashboard Screenshots & Features

### Key Metrics Dashboard
- **Total EGIDs**: Dynamic count with filter delta
- **Match Rate**: Color-coded percentage (green >90%, red <90%)
- **Mismatches**: Total and percentage
- **Changes**: Interim to Final modifications

### Interactive Charts
- **Bar Charts**: Existing vs Calculated ISRR comparison
- **Pie Charts**: Risk change distribution
- **Sankey Diagrams**: Visual flow from Interim to Final ISRR
- **Scatter Plots**: Data groups distribution
- **All charts are interactive**: Zoom, pan, hover for details

### Filtering Capabilities
- Filter by ISRR level (Multi-select)
- Filter by match status (All/Matched/Mismatched)
- Search across all data fields
- Column selection for custom views
- Real-time updates

### Export Options
- Download complete analysis (CSV/Excel)
- Download filtered results
- Download mismatches only
- Generate summary reports
- All exports respect active filters

---

## 🔍 Key Business Logic

### Data Group Classification
```
IF group has ANY transactional variable → Transactional Group
ELSE → Non-Transactional Group
```

### Nature of Data Rules
```
0 Trans + 1 Non-Trans → "1 Data group without Transactional Data"
1 Trans OR 2 Non-Trans → "1 Transactional Data group OR..."
2 Trans Groups → "Combination of 2 Transactional Data groups"
3+ Trans Groups → "Combination with 3 Transactional Data groups"
```

### Bank Data Classification
```
D4 = PII + Employee Data (both present)
D3 = Transactional Data present
D2 = PII present
```

### Final ISRR OR Logic
```
Rule applies if:
  (Volume matches) OR
  (Format matches) OR
  (Connectivity matches)

Priority:
  1. Most specific rules (fewest "Not considered")
  2. Higher risk impact
  3. Rules with modifiers
```

### Modifiers
```
ISRR + 1: Increases risk by one level (e.g., Moderate → High)
ISRR - 1: Decreases risk by one level (e.g., High → Moderate)
Direct: Sets specific ISRR level
```

---

## 📈 Performance

- Typical execution time: 2-5 minutes for 1,000 EGIDs
- Progress updates every 50 EGIDs
- Memory efficient (processes one EGID at a time)
- Dashboard loads instantly with cached data
- Interactive charts render smoothly (Plotly optimization)

---

## 🎯 Workflow: From Analysis to Dashboard

### Step 1: Prepare Data
1. Place all 5 Excel files in the `data/` folder
2. Ensure proper column names match `logic/config.py`

### Step 2: Run Analysis
```bash
python run.py
```
- Processes all EGIDs
- Generates results in `results/` folder
- Takes 2-5 minutes for typical datasets

### Step 3: Launch Dashboard
```bash
streamlit run dashboard.py
```
- Opens in browser automatically
- Loads pre-calculated results
- Interactive exploration begins

### Step 4: Explore Results
- Use filters to focus on specific segments
- Search for individual EGIDs
- Download filtered results
- Analyze mismatch patterns

### Step 5: Take Action
- Review mismatched EGIDs
- Export reports for stakeholders
- Update ISRR values where appropriate
- Document exceptions

---

## 🤝 Support

For issues or questions:
1. Check this README
2. Run `python utils/egid_diagnostic.py` for data issues
3. Review error messages in console
4. Check `logic/config.py` settings
5. Verify all files are in correct folders

---

## 📝 Version History

**v2.0** - Streamlit Dashboard & Folder Organization
- Added interactive Streamlit dashboard
- Organized project into logical folders (data, logic, utils, results)
- Enhanced visualizations with Plotly
- Real-time filtering and search
- Dynamic export capabilities
- Improved error handling

**v1.0** - Initial modular implementation
- Separated into 7 modules
- OR logic for final ISRR
- Comprehensive error handling
- Diagnostic tools included

---

## 🎯 Next Steps After Running Analysis

1. **Launch Dashboard** - `streamlit run dashboard.py`
2. **Explore Overview** - Review ISRR distributions and metrics
3. **Check Mismatches** - Investigate discrepancies in detail
4. **Analyze Flow** - Understand Interim→Final transformations
5. **Export Reports** - Download filtered results for stakeholders
6. **Validate Rules** - Verify business logic in `logic/config.py`
7. **Update Values** - Import calculated ISRR where appropriate
8. **Document Exceptions** - Note EGIDs requiring manual review

---

## 💡 Pro Tips

### Dashboard Tips
- **Use filters effectively**: Start broad, then narrow down
- **Export filtered data**: Apply filters before downloading
- **Bookmark views**: Save specific filter combinations
- **Check all tabs**: Each provides unique insights
- **Use search**: Fastest way to find specific EGIDs

### Analysis Tips
- **Run diagnostics first**: Catch data issues early
- **Verify config**: Check column names before running
- **Monitor progress**: Watch console for processing updates
- **Review samples**: Check sample outputs for accuracy
- **Back up results**: Save `results/` folder after each run

### Customization Tips
- **Adjust thresholds**: Modify business rules in config
- **Add new charts**: Dashboard is easily extensible
- **Custom exports**: Add new export formats as needed
- **Styling**: Customize dashboard CSS in `dashboard.py`
- **Logging**: Enable verbose mode in config

---

## 🚀 Advanced Features

### Dashboard Customization
Edit `dashboard.py` to add:
- New chart types
- Additional metrics
- Custom filtering logic
- New export formats
- Email integration

### Analysis Customization
Edit modules in `logic/` to:
- Modify calculation rules
- Add new data sources
- Change prioritization logic
- Implement new validators
- Add automated alerts

### Automation
Create scheduled runs:
```bash
# Linux/Mac crontab
0 2 * * * cd /path/to/isrr-analysis && python run.py

# Windows Task Scheduler
Run: python C:\path\to\isrr-analysis\run.py
Schedule: Daily at 2:00 AM
```

---

## 📦 Dependencies

### Core Dependencies
- **pandas** ≥1.5.0 - Data processing
- **numpy** ≥1.23.0 - Numerical operations
- **openpyxl** ≥3.0.0 - Excel file handling

### Dashboard Dependencies
- **streamlit** ≥1.28.0 - Interactive dashboard
- **plotly** ≥5.17.0 - Interactive visualizations

### Optional Dependencies
- **xlrd** ≥2.0.0 - Legacy Excel support

All dependencies in `requirements.txt` - install with:
```bash
pip install -r requirements.txt
```

---

## 🌟 Key Benefits

### Modular Architecture
✅ Easy maintenance and updates  
✅ Individual module testing  
✅ Clear separation of concerns  
✅ Scalable design  

### Interactive Dashboard
✅ Real-time data exploration  
✅ Beautiful visualizations  
✅ No coding required for analysis  
✅ Stakeholder-friendly interface  

### Organized Structure
✅ Input files in `data/`  
✅ Logic separated in `logic/`  
✅ Results isolated in `results/`  
✅ Utilities in `utils/`  

### Professional Output
✅ Publication-ready reports  
✅ Interactive charts for presentations  
✅ Multiple export formats  
✅ Audit trail for compliance  

---

**Ready to start?**

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis
python run.py

# Launch dashboard
streamlit run dashboard.py
```

🎉 **Enjoy your ISRR Analysis System with Interactive Dashboard!** 🎉

---

## 📞 Contact & Contributions

For feature requests, bug reports, or contributions, please document:
- Issue description
- Steps to reproduce
- Expected vs actual behavior
- System information
- Sample data (if applicable)

---

*Built with ❤️ for secure and efficient risk assessment*