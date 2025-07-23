import os
import pandas as pd
import numpy as np
from src.processing.cleaning import convert_csv
from src.processing.special_cleaning import tga_xy, normalize_tga
from src.processing.cleaning import auto_trim, interprolate_data
import matplotlib.pyplot as plt

# ----------------------- TGA -----------------------

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
    
    # Sort the processed data alphanumerically by sample name
    processed_data = sorted(processed_data, key=lambda df: df['sample'].iloc[0])
    
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

    # Auto-trim the data to find overlapping range
    if processed_data:
        # Use auto_trim to find overlapping range across all samples
        trimmed_data = auto_trim(processed_data, x_col='X')
        
        # Show summary of trimmed data
        print(f"\n=== Trimmed Data Summary ===")
        print(f"Total samples after trimming: {len(trimmed_data)}")
        # Print the overall trimmed data range (overlapping X range)
        if trimmed_data and not trimmed_data[0].empty:
            overlap_min = trimmed_data[0]['X'].min()
            overlap_max = trimmed_data[0]['X'].max()
            print(f"Trimmed data X range (overlapping): {overlap_min:.1f}°C to {overlap_max:.1f}°C")
        
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
                normalized_data = []
                
                for df in trimmed_data:
                    normalized_df = normalize_tga(df, y_col='Y')
                    normalized_data.append(normalized_df)
                
                # Show summary of normalized data
                print(f"\n=== Normalized Data Summary ===")
                print(f"Total samples after normalization: {len(normalized_data)}")
                
                if normalized_data:
                    print(f"First normalized DataFrame shape: {normalized_data[0].shape}")
                    print("First 5 rows of normalized data:")
                    print(normalized_data[0].head())
                    print("\nLast 5 rows of normalized data:")
                    print(normalized_data[0].tail())

                    # Interpolate the normalized data to a common grid
                    print(f"\n=== Interpolating Data ===")
                    interpolated_array = interprolate_data(normalized_data, x_col='X', y_col='Y', N=3000)
                    
                    print(f"Interpolated data shape: {interpolated_array.shape}")
                    print(f"Number of samples: {interpolated_array.shape[0]}")
                    print(f"Number of interpolated points per sample: {interpolated_array.shape[1]}")
                    
                    # Show some statistics about the interpolated data
                    print(f"\nInterpolated data statistics:")
                    print(f"Min value across all samples: {np.nanmin(interpolated_array):.4f}")
                    print(f"Max value across all samples: {np.nanmax(interpolated_array):.4f}")
                    print(f"Mean value across all samples: {np.nanmean(interpolated_array):.4f}")
                    
                    # Save the sample index mapping to a text file
                    sample_names = [df['sample'].iloc[0] for df in normalized_data]
                    mapping_file = "tga_sample_index_mapping.txt"
                    with open(mapping_file, 'w') as f:
                        f.write("Index\tSample Name\n")
                        f.write("-" * 30 + "\n")
                        for i, sample_name in enumerate(sample_names):
                            f.write(f"{i}\t{sample_name}\n")
                    print(f"\nSample index mapping saved to: {mapping_file}")
                    print("This mapping shows which row in the interpolated array corresponds to which sample.")
                    
                    # Plot the original normalized data
                    # Sort by sample name (alphanumeric)
                    # normalized_data_sorted = sorted(normalized_data, key=lambda df: df['sample'].iloc[0])
                    # plt.figure(figsize=(10, 6))
                    # for df in normalized_data_sorted:
                    #     plt.plot(df['X'], df['Y'], label=df['sample'].iloc[0], alpha=0.7)

                    # plt.xlabel('Temperature (°C)')
                    # plt.ylabel('Normalized Mass')
                    # plt.title('Normalized TGA Curves for All Samples')
                    # plt.legend(loc='best', fontsize='small', ncol=2)
                    # plt.tight_layout()
                    # plt.show()
                    
                    # Plot the interpolated data
                    # Get the x-axis values for the interpolated data
                    x_interp = np.linspace(normalized_data[0]['X'].min(), normalized_data[0]['X'].max(), 3000)
                    
                    plt.figure(figsize=(10, 6))
                    for i, sample_name in enumerate(sample_names):
                        plt.plot(x_interp, interpolated_array[i], label=sample_name, alpha=0.7)

                    plt.xlabel('Temperature (°C)')
                    plt.ylabel('Normalized Mass (Interpolated)')
                    plt.title('Interpolated TGA Curves for All Samples')
                    plt.legend(loc='best', fontsize='small', ncol=2)
                    plt.tight_layout()
                    plt.show()
else:
    print(f"Error: TGA folder {tga_folder} does not exist")

# ----------------------- DSC -----------------------

