import pandas as pd
import numpy as np

print("="*70)
print("DIAGNOSTIC: FINDING MISSING EGIDs")
print("="*70)

# Load the files
print("\n1. Loading files...")
rfimapped_df = pd.read_excel('rfimapped.xlsx')
results_df = pd.read_excel('complete_isrr_analysis.xlsx')  # Your output file

print(f"   rfimapped rows: {len(rfimapped_df)}")
print(f"   results rows: {len(results_df)}")

# STEP 1: Check column names
print("\n2. Checking column names...")
print(f"   rfimapped columns (first 10): {list(rfimapped_df.columns[:10])}")
print(f"   results columns (first 10): {list(results_df.columns[:10])}")

# Try to identify the EGID column in rfimapped
possible_egid_columns = [col for col in rfimapped_df.columns 
                         if 'egid' in col.lower() or 'id' in col.lower()]
print(f"   Possible EGID columns in rfimapped: {possible_egid_columns}")

# Identify the actual EGID column
egid_col_rfimapped = None
for col in ['EGID', 'egid', 'Egid', 'EgId', 'Engagementid', 'EngagementId', 'engagement_id']:
    if col in rfimapped_df.columns:
        egid_col_rfimapped = col
        print(f"   ✓ Found EGID column in rfimapped: '{egid_col_rfimapped}'")
        break

if not egid_col_rfimapped:
    print(f"   ⚠️ WARNING: Could not find standard EGID column!")
    print(f"   Available columns: {list(rfimapped_df.columns)}")
    egid_col_rfimapped = rfimapped_df.columns[0]  # Use first column
    print(f"   Using first column as EGID: '{egid_col_rfimapped}'")

# Identify EGID column in results
egid_col_results = None
for col in ['EGID', 'egid', 'Egid']:
    if col in results_df.columns:
        egid_col_results = col
        print(f"   ✓ Found EGID column in results: '{egid_col_results}'")
        break

# STEP 2: Extract EGID lists
print("\n3. Extracting EGID lists...")
rfimapped_egids = rfimapped_df[egid_col_rfimapped].unique()
results_egids = results_df[egid_col_results].unique()

print(f"   Unique EGIDs in rfimapped: {len(rfimapped_egids)}")
print(f"   Unique EGIDs in results: {len(results_egids)}")

# STEP 3: Check for duplicates
print("\n4. Checking for duplicates...")
rfimapped_duplicates = rfimapped_df[egid_col_rfimapped].duplicated().sum()
results_duplicates = results_df[egid_col_results].duplicated().sum()

print(f"   Duplicate EGIDs in rfimapped: {rfimapped_duplicates}")
print(f"   Duplicate EGIDs in results: {results_duplicates}")

if rfimapped_duplicates > 0:
    print(f"   ⚠️ WARNING: Duplicates found in rfimapped!")
    dup_egids = rfimapped_df[rfimapped_df[egid_col_rfimapped].duplicated(keep=False)][egid_col_rfimapped].unique()
    print(f"   Duplicate EGIDs (first 10): {dup_egids[:10]}")

# STEP 4: Check data types
print("\n5. Checking data types...")
print(f"   rfimapped EGID type: {rfimapped_df[egid_col_rfimapped].dtype}")
print(f"   results EGID type: {results_df[egid_col_results].dtype}")

# Show sample values
print(f"\n   Sample rfimapped EGIDs (first 5):")
for i, egid in enumerate(rfimapped_egids[:5]):
    print(f"      {i+1}. '{egid}' (type: {type(egid).__name__})")

print(f"\n   Sample results EGIDs (first 5):")
for i, egid in enumerate(results_egids[:5]):
    print(f"      {i+1}. '{egid}' (type: {type(egid).__name__})")

# STEP 5: Find missing EGIDs
print("\n6. Finding missing EGIDs...")

# Convert both to string for comparison (to handle type mismatches)
rfimapped_egids_str = set([str(x).strip() for x in rfimapped_egids])
results_egids_str = set([str(x).strip() for x in results_egids])

missing_in_results = rfimapped_egids_str - results_egids_str
extra_in_results = results_egids_str - rfimapped_egids_str

print(f"   EGIDs in rfimapped but NOT in results: {len(missing_in_results)}")
print(f"   EGIDs in results but NOT in rfimapped: {len(extra_in_results)}")

if len(missing_in_results) > 0:
    print(f"\n   ⚠️ MISSING EGIDs (in rfimapped but not in results):")
    for egid in list(missing_in_results)[:20]:  # Show first 20
        print(f"      - '{egid}'")
        
        # Find the original value in rfimapped
        original_matches = rfimapped_df[rfimapped_df[egid_col_rfimapped].astype(str).str.strip() == egid]
        if not original_matches.empty:
            original_value = original_matches.iloc[0][egid_col_rfimapped]
            print(f"        Original value: '{original_value}' (type: {type(original_value).__name__})")
            print(f"        Has leading/trailing spaces: {original_value != str(original_value).strip()}")

if len(extra_in_results) > 0:
    print(f"\n   ⚠️ EXTRA EGIDs (in results but not in rfimapped):")
    for egid in list(extra_in_results)[:20]:
        print(f"      - '{egid}'")

# STEP 6: Check for whitespace issues
print("\n7. Checking for whitespace issues...")

rfimapped_with_spaces = 0
for egid in rfimapped_egids[:100]:  # Check first 100
    if str(egid) != str(egid).strip():
        rfimapped_with_spaces += 1

print(f"   EGIDs with leading/trailing spaces in rfimapped (sample of 100): {rfimapped_with_spaces}")

# STEP 7: Check for NaN/None values
print("\n8. Checking for NaN/None values...")
rfimapped_nulls = rfimapped_df[egid_col_rfimapped].isna().sum()
results_nulls = results_df[egid_col_results].isna().sum()

print(f"   NULL/NaN EGIDs in rfimapped: {rfimapped_nulls}")
print(f"   NULL/NaN EGIDs in results: {results_nulls}")

# STEP 8: Deep dive into the missing EGIDs
if len(missing_in_results) > 0:
    print("\n9. Deep dive into missing EGIDs...")
    
    # Take first missing EGID and investigate
    first_missing = list(missing_in_results)[0]
    print(f"\n   Investigating missing EGID: '{first_missing}'")
    
    # Find it in rfimapped
    matches = rfimapped_df[rfimapped_df[egid_col_rfimapped].astype(str).str.strip() == first_missing]
    
    if not matches.empty:
        print(f"   Found in rfimapped at row index: {matches.index[0]}")
        print(f"   Full row data (first 10 columns):")
        for col in rfimapped_df.columns[:10]:
            print(f"      {col}: {matches.iloc[0][col]}")
    
    # Check if it exists in results under a different format
    print(f"\n   Checking if it exists in results with different format...")
    similar = results_df[results_df[egid_col_results].astype(str).str.contains(first_missing[:5], na=False)]
    if not similar.empty:
        print(f"   Found similar EGIDs in results:")
        for idx, row in similar.head(3).iterrows():
            print(f"      - '{row[egid_col_results]}'")

# STEP 9: Recommendations
print("\n" + "="*70)
print("RECOMMENDATIONS")
print("="*70)

if rfimapped_duplicates > 0:
    print("⚠️ 1. Remove or handle duplicate EGIDs in rfimapped.xlsx")

if rfimapped_df[egid_col_rfimapped].dtype != results_df[egid_col_results].dtype:
    print("⚠️ 2. Data type mismatch detected - ensure consistent data types")

if rfimapped_with_spaces > 0:
    print("⚠️ 3. Whitespace detected - clean EGID values")

if len(missing_in_results) > 0:
    print(f"⚠️ 4. CRITICAL: {len(missing_in_results)} EGIDs missing from results")
    print("   - Check if these EGIDs are being filtered out during processing")
    print("   - Verify the code loop is processing ALL EGIDs from rfimapped")

print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70)
