import os
import pandas as pd

# Root folder
root_dir = "/Users/markosulaja/Documents/trevco_test/"

# Walk through all subdirectories
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if this is the csv folder
    in_csv_folder = os.path.basename(dirpath) == "csv"

    for filename in filenames:
        file_path = os.path.join(dirpath, filename)

        print(f"\n--- Content of {os.path.relpath(file_path, root_dir)} ---")

        # If in csv folder and file is CSV, print first 5 rows
        if in_csv_folder and filename.lower().endswith('.csv'):
            try:
                df = pd.read_csv(file_path)
                print(df.head())
            except Exception as e:
                print(f"Error reading CSV {filename}: {e}")
        else:
            # Otherwise, print full content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    print(f.read())
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
