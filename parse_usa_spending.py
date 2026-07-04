import os
import pandas as pd

# The 3 massive CSV files in your directory
files = [
    'FY2026_All_Contracts_Full_20260506_1.csv',
    'FY2026_All_Contracts_Full_20260506_2.csv',
    'FY2026_All_Contracts_Full_20260506_3.csv'
]

ey_chunks = []
total_rows_processed = 0

print("Starting USAspending data extraction for EY...")
print("-" * 50)

for file in files:
    if not os.path.exists(file):
        print(f"Warning: Could not find {file} in the current directory. Skipping.")
        continue
        
    print(f"Processing file: {file}")
    
    # Reading in chunks of 100,000 rows to keep memory usage safe and low
    for chunk in pd.read_csv(file, chunksize=100000, low_memory=False):
        total_rows_processed += len(chunk)
        
        # Checking recipient name columns for EY variations
        if 'recipient_name' in chunk.columns:
            match = chunk[chunk['recipient_name'].str.contains("ERNST & YOUNG|ERNST AND YOUNG", case=False, na=False)]
            if not match.empty:
                ey_chunks.append(match)
                
    print(f"Finished {file}. Total rows scanned so far: {total_rows_processed:,}")
    print("-" * 50)

# Combine and save the filtered data
if ey_chunks:
    df_ey = pd.concat(ey_chunks, ignore_index=True)
    output_filename = 'ey_fy2026_extracted.csv'
    df_ey.to_csv(output_filename, index=False)
    
    print("\nExtraction Complete!")
    print(f"Total rows scanned across all files: {total_rows_processed:,}")
    print(f"Found {len(df_ey)} EY contract transactions.")
    print(f"Saved filtered data to a clean dataset: '{output_filename}'")
else:
    print("\nProcess finished, but no exact EY matches were found.")
    print("Double check if the CSV headers match or if the recipient naming convention is different.")