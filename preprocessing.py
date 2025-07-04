import os
import pandas as pd
from src.processing.cleaning import convert_csv
from src.processing.special_cleaning import tga_xy, normalize_tga
from src.processing.cleaning import trim_dataframe
import matplotlib.pyplot as plt

# # Get all subdirectories in the raw_data folder
# raw_data_path = "/Users/jessicaagyemang/Documents/raw_data/FTIR"
# data_directories = []

# if os.path.exists(raw_data_path):
#     # Get all subdirectories
#     for item in os.listdir(raw_data_path):
#         item_path = os.path.join(raw_data_path, item)
#         if os.path.isdir(item_path):
#             data_directories.append(item_path)
    
#     if data_directories:
#         print(f"Found {len(data_directories)} directories to process:")
#         for directory in data_directories:
#             print(f"  - {directory}")
        
#         # Call convert_csv function
#         results = convert_csv(data_directories)
#     else:
#         print("No subdirectories found in raw_data folder")
# else:
#     print(f"Error: Directory {raw_data_path} does not exist")


# Define the TGA folder path
tga_folder = "/Users/jessicaagyemang/Documents/raw_data/TGA"
# Call the tga_xy function
if os.path.exists(tga_folder):
    processed_data = tga_xy(tga_folder)
    
    print(f"Processed {len(processed_data)} TGA files")
    print("\n=== Data Structure ===")
    print(f"Type: {type(processed_data)}")
    print(f"Length: {len(processed_data)}")
    
    if processed_data:
        print(f"\nFirst DataFrame structure:")
        print(f"Shape: {processed_data[0].shape}")
        print(f"Columns: {list(processed_data[0].columns)}")
        print(f"Data types: {processed_data[0].dtypes}")
        
        # Show examples for LDPE and HDPE samples
        ldpe_samples = [df for df in processed_data if df['sample'].iloc[0].startswith('LDPE-')]
        hdpe_samples = [df for df in processed_data if df['sample'].iloc[0].startswith('HDPE-')]
        
        # if ldpe_samples:
        #     print(f"\n=== LDPE Sample Example ===")
        #     print(f"Sample name: {ldpe_samples[0]['sample'].iloc[0]}")
        #     print(f"Data shape: {ldpe_samples[0].shape}")
        #     print("First 5 rows:")
        #     print(ldpe_samples[0].head())
        #     print("\nLast 5 rows:")
        #     print(ldpe_samples[0].tail())
        
        # if hdpe_samples:
        #     print(f"\n=== HDPE Sample Example ===")
        #     print(f"Sample name: {hdpe_samples[0]['sample'].iloc[0]}")
        #     print(f"Data shape: {hdpe_samples[0].shape}")
        #     print("First 5 rows:")
        #     print(hdpe_samples[0].head())
        #     print("\nLast 5 rows:")
        #     print(hdpe_samples[0].tail())
        
        # # Summary statistics
        # print(f"\n=== Summary ===")
        # print(f"Total LDPE samples: {len(ldpe_samples)}")
        # print(f"Total HDPE samples: {len(hdpe_samples)}")
        
    else:
        print("No TGA data files found or processed")

    # Trim the data to x-values between 40 and 600
    if processed_data:
        print("\n=== Trimming Data ===")
        trimmed_data = []
        
        for df in processed_data:
            trimmed_df = trim_dataframe(df, x_min=40, x_max=600, x_col='X', y_col='Y', sample_col='sample')
            trimmed_data.append(trimmed_df)
            print(f"Trimmed {df['sample'].iloc[0]}: {df.shape[0]} -> {trimmed_df.shape[0]} data points")
        
        # Show summary of trimmed data
        print(f"\n=== Trimmed Data Summary ===")
        print(f"Total samples after trimming: {len(trimmed_data)}")
        
        if trimmed_data:
            print(f"First trimmed DataFrame shape: {trimmed_data[0].shape}")
            print("First 5 rows of trimmed data:")
            print(trimmed_data[0].head())
            print("\nLast 5 rows of trimmed data:")
            print(trimmed_data[0].tail())

            # # Show one example of LDPE and HDPE after trimming
            # ldpe_trimmed = [df for df in trimmed_data if not df.empty and df['sample'].iloc[0].startswith('LDPE-')]
            # hdpe_trimmed = [df for df in trimmed_data if not df.empty and df['sample'].iloc[0].startswith('HDPE-')]

            # if ldpe_trimmed:
            #     print("\n=== Example LDPE Trimmed Data ===")
            #     print(f"Sample name: {ldpe_trimmed[0]['sample'].iloc[0]}")
            #     print("First 5 rows:")
            #     print(ldpe_trimmed[0].head())
            #     print("\nLast 5 rows:")
            #     print(ldpe_trimmed[0].tail())

            # if hdpe_trimmed:
            #     print("\n=== Example HDPE Trimmed Data ===")
            #     print(f"Sample name: {hdpe_trimmed[0]['sample'].iloc[0]}")
            #     print("First 5 rows:")
            #     print(hdpe_trimmed[0].head())
            #     print("\nLast 5 rows:")
            #     print(hdpe_trimmed[0].tail())

            # # Summary statistics
            # print(f"\n=== Summary ===")
            # print(f"Total LDPE samples: {len(ldpe_trimmed)}")
            # print(f"Total HDPE samples: {len(hdpe_trimmed)}")

            # Normalize the trimmed data
            if trimmed_data:
                print("\n=== Normalizing Data ===")
                normalized_data = []
                
                for df in trimmed_data:
                    normalized_df = normalize_tga(df, y_col='Y')
                    normalized_data.append(normalized_df)
                    print(f"Normalized {df['sample'].iloc[0]}: Y_max = {df['Y'].max():.4f}")
                
                # Show summary of normalized data
                print(f"\n=== Normalized Data Summary ===")
                print(f"Total samples after normalization: {len(normalized_data)}")
                
                if normalized_data:
                    print(f"First normalized DataFrame shape: {normalized_data[0].shape}")
                    print("First 5 rows of normalized data:")
                    print(normalized_data[0].head())
                    print("\nLast 5 rows of normalized data:")
                    print(normalized_data[0].tail())

                    # Sort by sample name (alphanumeric)
                    normalized_data_sorted = sorted(normalized_data, key=lambda df: df['sample'].iloc[0])
                    plt.figure(figsize=(10, 6))
                    for df in normalized_data_sorted:
                        plt.plot(df['X'], df['Y'], label=df['sample'].iloc[0], alpha=0.7)

                    plt.xlabel('Temperature (°C)')
                    plt.ylabel('Normalized Mass')
                    plt.title('Normalized TGA Curves for All Samples')
                    plt.legend(loc='best', fontsize='small', ncol=2)
                    plt.tight_layout()
                    plt.show()
else:
    print(f"Error: TGA folder {tga_folder} does not exist")


