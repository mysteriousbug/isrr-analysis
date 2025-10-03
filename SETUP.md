# ISRR Analysis System - Setup Guide

## 📋 Quick Setup (5 Minutes)

Follow these steps to set up your ISRR Analysis System with interactive dashboard.

---

## Step 1: Create Project Structure

Create the following folder structure:

```
isrr-analysis/
├── data/                   # Create this folder
├── logic/                  # Create this folder
├── utils/                  # Create this folder
└── results/                # Will be auto-created
```

### Commands:

**Windows:**
```cmd
mkdir isrr-analysis
cd isrr-analysis
mkdir data
mkdir logic
mkdir utils
```

**Mac/Linux:**
```bash
mkdir -p isrr-analysis/{data,logic,utils}
cd isrr-analysis
```

---

## Step 2: Add Python Files

Place these files in the **root** folder (`isrr-analysis/`):
- `run.py`
- `dashboard.py`
- `requirements.txt`
- `README.md`

Place these files in the **logic/** folder:
- `__init__.py`
- `config.py`
- `data_loader.py`
- `variable_analyzer.py`
- `interim_isrr_calculator.py`
- `final_isrr_calculator.py`
- `comparator.py`

Place this file in the **utils/** folder:
- `egid_diagnostic.py`

---

## Step 3: Add Your Data Files

Place these **5 Excel files** in the **data/** folder:
- `variables.xlsx`
- `rfimapped.xlsx`
- `mainrfi.xlsx`
- `interimisrr.xlsx`
- `finalisrr.xlsx`

### Verify Data Files:
```bash
# Check if files exist
ls data/
```

You should see all 5 Excel files listed.

---

## Step 4: Install Python Dependencies

### Option A: Using pip (Recommended)
```bash
pip install -r requirements.txt
```

### Option B: Install manually
```bash
pip install pandas numpy openpyxl streamlit plotly xlrd
```

### Verify Installation:
```bash
python -c "import pandas, streamlit, plotly; print('✓ All dependencies installed!')"
```

---

## Step 5: Verify Configuration

Open `logic/config.py` and verify column names match your Excel files:

```python
# Check these match your mainrfi.xlsx columns
MAINRFI_COLUMNS = {
    'volume': 'Tpmaxrecordscanprocess',    # ← Verify this
    'format': 'Isdataelecform',            # ← Verify this
    'connectivity': 'Systemconnectivity',   # ← Verify this
    'existing_isrr': 'Isrrvalue',          # ← Verify this
}
```

**How to verify:**
1. Open your `data/mainrfi.xlsx` file
2. Check the exact column names in the first row
3. Update `logic/config.py` if names don't match

---

## Step 6: Run Your First Analysis

```bash
python run.py
```

### What to expect:
- Processing time: 2-5 minutes for 1,000 EGIDs
- Progress updates every 50 EGIDs
- Results saved to `results/` folder (auto-created)

### Success indicators:
- ✓ All files loaded successfully
- ✓ All EGIDs processed
- ✓ Files created in `results/` folder

---

## Step 7: Launch the Dashboard

```bash
streamlit run dashboard.py
```

### What to expect:
- Browser opens automatically to `http://localhost:8501`
- Dashboard loads with your analysis results
- Interactive charts and filters ready to use

### If browser doesn't open:
Manually navigate to: `http://localhost:8501`

---

## 🎉 You're All Set!

Your ISRR Analysis System is now running with:
- ✅ Automated analysis pipeline
- ✅ Interactive Streamlit dashboard
- ✅ Real-time visualizations
- ✅ Dynamic filtering and export

---

## 🔧 Troubleshooting Setup

### Problem: "ModuleNotFoundError: No module named 'logic'"

**Solution:**
Run Python from the **root** folder (`isrr-analysis/`), not from inside subfolders.

```bash
# Wrong:
cd logic
python ../run.py  # ❌ Don't do this

# Correct:
cd isrr-analysis  # Go to root
python run.py     # ✓ Run from root
```

---

### Problem: "FileNotFoundError: data/variables.xlsx"

**Solution:**
Ensure Excel files are in the `data/` folder:

```bash
# Check file location
ls data/variables.xlsx  # Should exist
```

If file is in wrong location, move it:
```bash
mv variables.xlsx data/  # Move to data folder
```

---

### Problem: "Column 'Isrrvalue' not found"

**Solution:**
Your Excel file has different column names. Update `logic/config.py`:

1. Open your `mainrfi.xlsx` file
2. Note the exact column names
3. Update `MAINRFI_COLUMNS` in `logic/config.py`

Example:
```python
# If your column is named 'ISRR_Value' instead of 'Isrrvalue'
MAINRFI_COLUMNS = {
    'existing_isrr': 'ISRR_Value',  # Update this
}
```

---

### Problem: "Streamlit command not found"

**Solution:**
Reinstall streamlit:
```bash
pip install --upgrade streamlit
```

Or use full path:
```bash
python -m streamlit run dashboard.py
```

---

### Problem: Dashboard shows "No data available"

**Solution:**
Run the analysis first:
```bash
python run.py  # Generate results first
streamlit run dashboard.py  # Then open dashboard
```

---

### Problem: Missing EGIDs in results

**Solution:**
Run the diagnostic tool:
```bash
python utils/egid_diagnostic.py
```

This will identify:
- Data type mismatches
- Whitespace issues
- Duplicate EGIDs
- Column name problems

---

## 📁 Final Folder Structure

After setup, your project should look like this:

```
isrr-analysis/
│
├── run.py                          ✓ Root level
├── dashboard.py                    ✓ Root level
├── requirements.txt                ✓ Root level
├── README.md                       ✓ Root level
│
├── data/                           ✓ Your Excel files here
│   ├── variables.xlsx
│   ├── rfimapped.xlsx
│   ├── mainrfi.xlsx
│   ├── interimisrr.xlsx
│   └── finalisrr.xlsx
│
├── logic/                          ✓ All logic modules
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── variable_analyzer.py
│   ├── interim_isrr_calculator.py
│   ├── final_isrr_calculator.py
│   └── comparator.py
│
├── utils/                          ✓ Utility scripts
│   └── egid_diagnostic.py
│
└── results/                        ✓ Auto-generated outputs
    ├── complete_isrr_analysis.xlsx
    ├── isrr_mismatches.xlsx
    └── isrr_summary_report.txt
```

---

## ✅ Verification Checklist

Before running, verify:

- [ ] All Python files in correct folders
- [ ] All 5 Excel files in `data/` folder
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Running from **root** folder (`isrr-analysis/`)
- [ ] Column names in `logic/config.py` match your Excel files

---

## 🚀 Next Steps

1. **First Run:** `python run.py`
2. **Launch Dashboard:** `streamlit run dashboard.py`
3. **Explore Results:** Use filters and interactive charts
4. **Customize:** Edit `logic/config.py` for your needs
5. **Share:** Export reports from dashboard

---

## 💡 Tips for Success

1. **Always run from root folder** - Don't cd into subfolders
2. **Verify column names first** - Prevents most errors
3. **Run diagnostic if issues** - `python utils/egid_diagnostic.py`
4. **Check console output** - Shows progress and errors
5. **Update config for changes** - All settings in `logic/config.py`

---

## 📞 Need Help?

Check:
1. This SETUP.md file
2. Main README.md file
3. Error messages in console
4. `logic/config.py` settings
5. Run diagnostic: `python utils/egid_diagnostic.py`

---

**Ready to analyze? Run: `python run.py`** 🚀
