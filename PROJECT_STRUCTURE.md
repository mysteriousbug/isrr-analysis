# 📂 ISRR Analysis System - Project Structure

## 🏗️ Complete Folder Layout

```
isrr-analysis/                          🏠 ROOT DIRECTORY
│
├── 🚀 EXECUTION FILES (Root Level)
│   ├── run.py                          ⚙️ Main analysis execution script
│   ├── dashboard.py                    📊 Streamlit interactive dashboard
│   ├── requirements.txt                📦 Python dependencies
│   ├── README.md                       📖 Main documentation
│   └── SETUP.md                        🔧 Setup instructions
│
├── 📁 data/                            💾 INPUT DATA FOLDER
│   │                                   (Place all 5 Excel files here)
│   ├── variables.xlsx                  📋 Variable metadata (160+ variables)
│   ├── rfimapped.xlsx                  ✅ TRUE/FALSE mappings per EGID
│   ├── mainrfi.xlsx                    🏦 Core RFI data & existing ISRR
│   ├── interimisrr.xlsx               📐 Interim ISRR calculation rules
│   └── finalisrr.xlsx                 🎯 Final ISRR modifier rules
│
├── 📁 logic/                           🧠 BUSINESS LOGIC MODULES
│   │                                   (All calculation & processing code)
│   ├── __init__.py                     📦 Package initializer
│   ├── config.py                       ⚙️ Configuration & constants
│   ├── data_loader.py                  📥 Load & clean data
│   ├── variable_analyzer.py            🔍 Group & classify variables
│   ├── interim_isrr_calculator.py     📊 Calculate interim ISRR
│   ├── final_isrr_calculator.py       🎯 Calculate final ISRR (OR logic)
│   └── comparator.py                   📈 Compare & export results
│
├── 📁 utils/                           🛠️ UTILITY SCRIPTS
│   │                                   (Helper & diagnostic tools)
│   └── egid_diagnostic.py              🔬 Troubleshoot missing EGIDs
│
└── 📁 results/                         📤 OUTPUT FILES (Auto-generated)
    │                                   (Created automatically after run.py)
    ├── complete_isrr_analysis.xlsx     📊 Complete analysis results
    ├── isrr_mismatches.xlsx           ⚠️ Mismatched ISRR records
    └── isrr_summary_report.txt         📄 Text summary report
```

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         INPUT DATA                              │
│                      (data/ folder)                             │
└─────────────────────────────────────────────────────────────────┘
                                ↓
        ┌───────────────────────┴───────────────────────┐
        │                                                │
        ↓                                                ↓
┌──────────────────┐                          ┌──────────────────┐
│ variables.xlsx   │                          │ mainrfi.xlsx     │
│ rfimapped.xlsx   │                          │ interimisrr.xlsx │
│                  │                          │ finalisrr.xlsx   │
└────────┬─────────┘                          └────────┬─────────┘
         │                                             │
         └──────────────────┬──────────────────────────┘
                            ↓
        ┌───────────────────────────────────────────────┐
        │         LOGIC MODULES PROCESSING              │
        │            (logic/ folder)                    │
        │                                               │
        │  1. data_loader.py        → Load & Clean     │
        │  2. variable_analyzer.py   → Group Variables │
        │  3. interim_isrr_calculator.py → Interim ISRR│
        │  4. final_isrr_calculator.py → Final ISRR    │
        │  5. comparator.py          → Compare & Export│
        └───────────────────┬───────────────────────────┘
                            ↓
        ┌───────────────────────────────────────────────┐
        │              OUTPUT FILES                     │
        │            (results/ folder)                  │
        │                                               │
        │  • complete_isrr_analysis.xlsx               │
        │  • isrr_mismatches.xlsx                      │
        │  • isrr_summary_report.txt                   │
        └───────────────────┬───────────────────────────┘
                            ↓
        ┌───────────────────────────────────────────────┐
        │         INTERACTIVE DASHBOARD                 │
        │           (dashboard.py)                      │
        │                                               │
        │  → Visualizations with Plotly                │
        │  → Real-time filtering                       │
        │  → Dynamic exports                           │
        └───────────────────────────────────────────────┘
```

---

## 🎯 Module Responsibilities

### **Root Level Files**

| File | Purpose | When to Use |
|------|---------|-------------|
| `run.py` | Execute complete analysis | Start here - main entry point |
| `dashboard.py` | Interactive dashboard | After run.py - view results |
| `requirements.txt` | Python dependencies | First time setup |
| `README.md` | Complete documentation | Reference guide |
| `SETUP.md` | Setup instructions | Initial setup |

### **data/ Folder**

| File | Contains | Used By |
|------|----------|---------|
| `variables.xlsx` | Variable metadata (name, group, type, category, classification) | variable_analyzer.py |
| `rfimapped.xlsx` | TRUE/FALSE for 160 variables per EGID | variable_analyzer.py |
| `mainrfi.xlsx` | EGID details (volume, format, connectivity, existing ISRR) | final_isrr_calculator.py, comparator.py |
| `interimisrr.xlsx` | Rules for interim ISRR calculation | interim_isrr_calculator.py |
| `finalisrr.xlsx` | Rules for final ISRR with modifiers | final_isrr_calculator.py |

### **logic/ Folder**

| Module | Responsibility | Input | Output |
|--------|---------------|-------|--------|
| `config.py` | Configuration & constants | - | Settings for all modules |
| `data_loader.py` | Load & clean data | 5 Excel files | Clean DataFrames |
| `variable_analyzer.py` | Group variables by EGID | variables.xlsx, rfimapped.xlsx | egid_analysis dict |
| `interim_isrr_calculator.py` | Calculate interim ISRR | egid_analysis, interimisrr.xlsx | interim_results dict |
| `final_isrr_calculator.py` | Calculate final ISRR | interim_results, mainrfi.xlsx, finalisrr.xlsx | final_results dict |
| `comparator.py` | Compare & export | All results, mainrfi.xlsx | Excel files in results/ |

### **utils/ Folder**

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `egid_diagnostic.py` | Troubleshoot missing EGIDs | When EGIDs are missing from output |

### **results/ Folder** (Auto-generated)

| File | Contains | Used By |
|------|----------|---------|
| `complete_isrr_analysis.xlsx` | All EGIDs with calculated ISRR | Dashboard, stakeholders |
| `isrr_mismatches.xlsx` | Only mismatched EGIDs | Review & validation |
| `isrr_summary_report.txt` | Summary statistics | Quick overview |

---

## 🚀 Execution Sequence

### **Standard Workflow**

```
1. PREPARE
   └─→ Place 5 Excel files in data/ folder

2. CONFIGURE  
   └─→ Verify settings in logic/config.py

3. INSTALL
   └─→ pip install -r requirements.txt

4. ANALYZE
   └─→ python run.py
       ├─→ Loads data from data/
       ├─→ Processes with logic/ modules
       └─→ Saves results to results/

5. VISUALIZE
   └─→ streamlit run dashboard.py
       ├─→ Loads results from results/
       └─→ Interactive exploration
```

### **Troubleshooting Workflow**

```
1. ISSUE DETECTED
   └─→ Missing EGIDs or errors

2. RUN DIAGNOSTIC
   └─→ python utils/egid_diagnostic.py
       ├─→ Checks data quality
       ├─→ Identifies issues
       └─→ Suggests fixes

3. FIX ISSUES
   └─→ Update data/ files or logic/config.py

4. RE-RUN
   └─→ python run.py
```

---

## 📦 File Dependencies

```
run.py
  ├── logic/data_loader.py
  │     └── logic/config.py
  │           └── data/*.xlsx
  │
  ├── logic/variable_analyzer.py
  │     ├── logic/config.py
  │     └── data/variables.xlsx, rfimapped.xlsx
  │
  ├── logic/interim_isrr_calculator.py
  │     ├── logic/config.py
  │     └── data/interimisrr.xlsx
  │
  ├── logic/final_isrr_calculator.py
  │     ├── logic/config.py
  │     └── data/mainrfi.xlsx, finalisrr.xlsx
  │
  └── logic/comparator.py
        ├── logic/config.py
        └── results/*.xlsx

dashboard.py
  ├── logic/config.py
  └── results/*.xlsx
```

---

## 🎨 Dashboard Architecture

```
dashboard.py
  │
  ├── Sidebar (Filters)
  │   ├── ISRR Level Filter (Multi-select)
  │   ├── Match Status Filter (Radio)
  │   └── Apply to all tabs
  │
  ├── Tab 1: Overview
  │   ├── Key Metrics (4 cards)
  │   ├── ISRR Comparison Chart
  │   ├── Risk Changes Pie Chart
  │   ├── Data Groups Scatter Plot
  │   └── Summary Statistics
  │
  ├── Tab 2: Mismatches
  │   ├── Mismatch Count
  │   ├── Top Patterns
  │   ├── Severity Chart
  │   ├── Searchable Table
  │   └── Download Button
  │
  ├── Tab 3: Flow Analysis
  │   ├── Sankey Diagram (Interim→Final)
  │   └── Modifier Distribution
  │
  ├── Tab 4: Data Table
  │   ├── Search Bar
  │   ├── Column Selector
  │   └── Full Results Table
  │
  └── Tab 5: Export
      ├── Download Complete Analysis
      ├── Download Mismatches
      └── Download Summary Report
```

---

## 🔑 Key Concepts

### **Module Communication**

```
config.py
   ↓ (provides settings to)
All Modules
   ↓ (pass data between)
run.py (orchestrator)
   ↓ (generates)
results/
   ↓ (consumed by)
dashboard.py
```

### **Data Transformation Pipeline**

```
Raw Excel Files
   ↓ data_loader.py
Cleaned DataFrames
   ↓ variable_analyzer.py
Grouped Variables per EGID
   ↓ interim_isrr_calculator.py
Interim ISRR Results
   ↓ final_isrr_calculator.py
Final ISRR Results
   ↓ comparator.py
Excel Reports + Dashboard Data
```

---

## 💡 Best Practices

### **File Organization**

✅ **DO:**
- Keep all Excel files in `data/` folder
- Run Python scripts from root folder
- Let system auto-create `results/` folder
- Update only `logic/config.py` for settings

❌ **DON'T:**
- Put Excel files in root folder
- Run scripts from inside subfolders
- Manually create `results/` folder
- Hardcode settings in module files

### **Module Updates**

✅ **DO:**
- Update `logic/config.py` for column names
- Modify business rules in `logic/config.py`
- Add new features in appropriate logic module

❌ **DON'T:**
- Scatter settings across multiple files
- Hardcode values in calculation modules
- Mix configuration with business logic

---

## 🎯 Quick Reference

### **Common Tasks**

| Task | Command | Location |
|------|---------|----------|
| Run analysis | `python run.py` | Root folder |
| Open dashboard | `streamlit run dashboard.py` | Root folder |
| Troubleshoot | `python utils/egid_diagnostic.py` | Root folder |
| Update settings | Edit `logic/config.py` | logic/ folder |
| Add data | Copy Excel to `data/` | data/ folder |
| View results | Open files in `results/` | results/ folder |

### **Important Paths**

```python
# In code, use these from config.py:
config.DATA_DIR          # → 'data/'
config.RESULTS_DIR       # → 'results/'
config.INPUT_FILES       # → dict of input file paths
config.OUTPUT_FILES      # → dict of output file names
```

---

## 📊 Capacity & Performance

| Metric | Typical Value | Notes |
|--------|--------------|-------|
| EGIDs processed | 1,000 - 10,000 | Scales linearly |
| Variables tracked | 160+ | Configurable |
| Processing time | 2-5 min / 1000 EGIDs | Depends on system |
| Dashboard load time | < 5 seconds | With cached data |
| Memory usage | < 500 MB | For typical datasets |

---

**This structure ensures:**
- 🎯 Clear separation of concerns
- 📁 Easy to navigate
- 🔧 Simple to maintain
- 📈 Scalable for growth
- 🚀 Fast to execute

---

*Organized for success!* ✨