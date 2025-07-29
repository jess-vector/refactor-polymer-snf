import os
import pandas as pd
import numpy as np
from src.processing.cleaning import convert_csv
from src.processing.special_cleaning import tga_xy, normalize_tga
from src.processing.cleaning import auto_trim, interprolate_data, select_trim
import matplotlib.pyplot as plt

# Create output directories for processed data
output_dir = "processed_data"
tga_output_dir = os.path.join(output_dir, "tga")
dsc_output_dir = os.path.join(output_dir, "dsc")

# Create directories if they don't exist
os.makedirs(tga_output_dir, exist_ok=True)
os.makedirs(dsc_output_dir, exist_ok=True)

print(f"Created output directories:")
print(f"  - TGA data: {tga_output_dir}")
print(f"  - DSC data: {dsc_output_dir}")

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
tga_filepath = "/Users/jessicaagyemang/Documents/raw_data/TGA"
# Call the tga_xy function
if os.path.exists(tga_filepath):
    processed_data = tga_xy(tga_filepath)
    
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
                    
                    # Get sample names for display
                    sample_names = [df['sample'].iloc[0] for df in normalized_data]
                    print(f"\nTGA Processing Summary:")
                    print(f"  - Number of samples: {len(sample_names)}")
                    print(f"  - Interpolation points: {interpolated_array.shape[1]}")
                    print(f"  - Temperature range: {normalized_data[0]['X'].min():.1f}°C to {normalized_data[0]['X'].max():.1f}°C")
                    print(f"  - Sample names: {sample_names}")
                    
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
                    
                    # Store TGA data for later plotting
                    tga_plot_data = {
                        'x': x_interp,
                        'y': interpolated_array,
                        'sample_names': sample_names,
                        'title': 'Interpolated TGA Curves for All Samples',
                        'ylabel': 'Normalized Mass (Interpolated)'
                    }
                    
                    print("\nTGA data processing complete!")
else:
    print(f"Error: TGA folder {tga_filepath} does not exist")

# ----------------------- DSC -----------------------

# Define the DSC folder path
dsc_filepath = "/Users/jessicaagyemang/Documents/raw_data/DSC"
# Check if the DSC folder exists
if os.path.exists(dsc_filepath):
    # List files in DSC folder for debugging
    dsc_files = [f for f in os.listdir(dsc_filepath) if f.endswith('.csv')]
    print(f"\n=== DSC Folder Contents ===")
    print(f"Found {len(dsc_files)} CSV files in DSC folder:")
    for f in dsc_files:
        print(f"  - {f}")
    print()
    # Call the dsc_xy function to process DSC files
    try:
        from src.processing.special_cleaning import dsc_xy
    except ImportError:
        print("dsc_xy function not found in special_cleaning. Please implement or import it.")
        dsc_xy = None

    if dsc_xy is not None:
        dsc_processed_data = dsc_xy(dsc_filepath)

        # Sort the processed data alphanumerically by sample name if not empty
        if dsc_processed_data:
            dsc_processed_data = sorted(dsc_processed_data, key=lambda df: df['sample'].iloc[0])
            print(f"Processed {len(dsc_processed_data)} DSC files")
            print("\n=== DSC Data Structure ===")
            print(f"Type: {type(dsc_processed_data)}")
            print(f"Length: {len(dsc_processed_data)}")
            print(f"First DataFrame structure:")
            print(f"Shape: {dsc_processed_data[0].shape}")
            print(f"Columns: {list(dsc_processed_data[0].columns)}")
            print(f"Data types: {dsc_processed_data[0].dtypes}")

            # Trim the data to specific temperature range (60-180°C for DSC)
            dsc_trimmed_data = []
            for df in dsc_processed_data:
                trimmed_df = select_trim(df, x_min=60, x_max=180, x_col='X', y_col='Y', sample_col='sample')
                dsc_trimmed_data.append(trimmed_df)
            print(f"\n=== Trimmed DSC Data Summary ===")
            print(f"Total samples after trimming: {len(dsc_trimmed_data)}")
            if dsc_trimmed_data and not dsc_trimmed_data[0].empty:
                overlap_min = dsc_trimmed_data[0]['X'].min()
                overlap_max = dsc_trimmed_data[0]['X'].max()
                print(f"Trimmed DSC data X range (overlapping): {overlap_min:.1f}°C to {overlap_max:.1f}°C")
            if dsc_trimmed_data:
                print(f"First trimmed DSC DataFrame shape: {dsc_trimmed_data[0].shape}")
                print("First 5 rows of trimmed DSC data:")
                print(dsc_trimmed_data[0].head())
                
                # Interpolate the DSC data to a common grid
                print(f"\n=== Interpolating DSC Data ===")
                dsc_interpolated_array = interprolate_data(dsc_trimmed_data, x_col='X', y_col='Y', N=3000)
                
                print(f"Interpolated DSC data shape: {dsc_interpolated_array.shape}")
                print(f"Number of samples: {dsc_interpolated_array.shape[0]}")
                print(f"Number of interpolated points per sample: {dsc_interpolated_array.shape[1]}")
                
                # Show some statistics about the interpolated DSC data
                print(f"\nInterpolated DSC data statistics:")
                print(f"Min value across all samples: {np.nanmin(dsc_interpolated_array):.4f}")
                print(f"Max value across all samples: {np.nanmax(dsc_interpolated_array):.4f}")
                print(f"Mean value across all samples: {np.nanmean(dsc_interpolated_array):.4f}")
                
                # Save the DSC sample index mapping
                dsc_sample_names = [df['sample'].iloc[0] for df in dsc_trimmed_data if not df.empty]
                dsc_mapping_file = os.path.join(dsc_output_dir, "dsc_sample_index_mapping.txt")
                with open(dsc_mapping_file, 'w') as f:
                    f.write("Index\tSample Name\n")
                    f.write("-" * 30 + "\n")
                    for i, sample_name in enumerate(dsc_sample_names):
                        f.write(f"{i}\t{sample_name}\n")
                print(f"\nDSC sample index mapping saved to: {dsc_mapping_file}")
                
                # Save the interpolated DSC data
                dsc_data_file = os.path.join(dsc_output_dir, "interpolated_dsc_data.npy")
                np.save(dsc_data_file, dsc_interpolated_array)
                print(f"Interpolated DSC data saved to: {dsc_data_file}")
                
                # Save metadata about the DSC data
                dsc_metadata = {
                    'num_samples': dsc_interpolated_array.shape[0],
                    'num_points': dsc_interpolated_array.shape[1],
                    'x_range': [dsc_trimmed_data[0]['X'].min(), dsc_trimmed_data[0]['X'].max()],
                    'sample_names': dsc_sample_names,
                    'data_type': 'DSC',
                    'trim_range': [60, 180],  # Temperature range used for trimming
                    'interpolation_points': 3000
                }
                
                dsc_metadata_file = os.path.join(dsc_output_dir, "dsc_metadata.npz")
                np.savez(dsc_metadata_file, **dsc_metadata)
                print(f"DSC metadata saved to: {dsc_metadata_file}")
                
                # Save sample names as a separate text file for easy reading
                dsc_samples_file = os.path.join(dsc_output_dir, "dsc_sample_names.txt")
                with open(dsc_samples_file, 'w') as f:
                    for i, sample_name in enumerate(dsc_sample_names):
                        f.write(f"{i}: {sample_name}\n")
                print(f"DSC sample names saved to: {dsc_samples_file}")
                
                # Plot the interpolated DSC data
                x_interp_dsc = np.linspace(dsc_trimmed_data[0]['X'].min(), dsc_trimmed_data[0]['X'].max(), 3000)
                
                # Store DSC data for later plotting
                dsc_plot_data = {
                    'x': x_interp_dsc,
                    'y': dsc_interpolated_array,
                    'sample_names': dsc_sample_names,
                    'title': 'Interpolated DSC Curves for All Samples',
                    'ylabel': 'Heat Flow (W/g) - Interpolated'
                }
                
                print("\nDSC data processing complete!")
        else:
            print("No DSC data files found or processed")
    else:
        print("dsc_xy function is not available.")
else:
    print(f"Error: DSC folder {dsc_filepath} does not exist")

# ----------------------- Summary -----------------------

print(f"\n{'='*50}")
print("PROCESSING SUMMARY")
print(f"{'='*50}")

# Check what was saved
if os.path.exists(tga_output_dir):
    tga_files = os.listdir(tga_output_dir)
    print(f"\nTGA data saved in: {tga_output_dir}")
    print("Files created:")
    for file in tga_files:
        file_path = os.path.join(tga_output_dir, file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size} bytes)")

if os.path.exists(dsc_output_dir):
    dsc_files = os.listdir(dsc_output_dir)
    print(f"\nDSC data saved in: {dsc_output_dir}")
    print("Files created:")
    for file in dsc_files:
        file_path = os.path.join(dsc_output_dir, file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size} bytes)")

print(f"\n{'='*50}")
print("Data files are ready for further analysis!")
print(f"{'='*50}")

# ----------------------- Interactive Plotting -----------------------

# Check if we have both TGA and DSC data to plot
if 'tga_plot_data' in locals() and 'dsc_plot_data' in locals():
    print("\nCreating interactive plot with navigation...")
    
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Button
    
    # Create the main figure and subplot
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(bottom=0.15)  # Make room for buttons
    
    # Create a class to handle the interactive plotting
    class InteractivePlotter:
        def __init__(self, tga_data, dsc_data):
            self.tga_data = tga_data
            self.dsc_data = dsc_data
            self.current_data = 'tga'
            self.plot_data = tga_data
            self.ax = ax
            self.fig = fig
        
        def plot_current_data(self):
            self.ax.clear()
            for i, sample_name in enumerate(self.plot_data['sample_names']):
                self.ax.plot(self.plot_data['x'], self.plot_data['y'][i], label=sample_name, alpha=0.7)
            
            self.ax.set_xlabel('Temperature (°C)')
            self.ax.set_ylabel(self.plot_data['ylabel'])
            self.ax.set_title(self.plot_data['title'])
            self.ax.legend(loc='best', fontsize='small', ncol=2)
            self.ax.grid(True, alpha=0.3)
            plt.draw()
        
        def switch_to_tga(self, event):
            self.current_data = 'tga'
            self.plot_data = self.tga_data
            self.plot_current_data()
            print("Switched to TGA data")
        
        def switch_to_dsc(self, event):
            self.current_data = 'dsc'
            self.plot_data = self.dsc_data
            self.plot_current_data()
            print("Switched to DSC data")
    
    # Create the plotter instance
    plotter = InteractivePlotter(tga_plot_data, dsc_plot_data)
    
    # Create buttons
    ax_tga = plt.axes([0.2, 0.05, 0.15, 0.075])
    ax_dsc = plt.axes([0.65, 0.05, 0.15, 0.075])
    
    btn_tga = Button(ax_tga, 'Show TGA')
    btn_dsc = Button(ax_dsc, 'Show DSC')
    
    # Connect button events
    btn_tga.on_clicked(plotter.switch_to_tga)
    btn_dsc.on_clicked(plotter.switch_to_dsc)
    
    # Plot initial data (TGA)
    plotter.plot_current_data()
    
    plt.show()
    print("Interactive plot created! Use the buttons to switch between TGA and DSC data.")

elif 'tga_plot_data' in locals():
    print("\nOnly TGA data available - showing TGA plot...")
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12, 8))
    for i, sample_name in enumerate(tga_plot_data['sample_names']):
        plt.plot(tga_plot_data['x'], tga_plot_data['y'][i], label=sample_name, alpha=0.7)
    
    plt.xlabel('Temperature (°C)')
    plt.ylabel(tga_plot_data['ylabel'])
    plt.title(tga_plot_data['title'])
    plt.legend(loc='best', fontsize='small', ncol=2)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

elif 'dsc_plot_data' in locals():
    print("\nOnly DSC data available - showing DSC plot...")
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12, 8))
    for i, sample_name in enumerate(dsc_plot_data['sample_names']):
        plt.plot(dsc_plot_data['x'], dsc_plot_data['y'][i], label=sample_name, alpha=0.7)
    
    plt.xlabel('Temperature (°C)')
    plt.ylabel(dsc_plot_data['ylabel'])
    plt.title(dsc_plot_data['title'])
    plt.legend(loc='best', fontsize='small', ncol=2)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

else:
    print("\nNo plot data available to display.")
