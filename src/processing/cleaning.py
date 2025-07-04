# Generic cleaning functions for all data modalities


# FUNCT1 check if data is in .csv format, if not convert to .csv function (if not already). All sample data is saved in a folder titled with relevant modality. 
import os
import pandas as pd
import glob
from pathlib import Path


def convert_csv(data_directories):
    """
    Convert non-CSV files to CSV format in specified directories.
    
    Args:
        data_directories (list): List of directory paths to process
                                (e.g., ['raw_data/TGA/', 'raw_data/DSC/', 'raw_data/FTIR/', 'raw_data/Rheology/'])
    
    Returns:
        dict: Summary of conversion results for each directory
    """
    conversion_summary = {}
    
    for directory in data_directories:
        if not os.path.exists(directory):
            print(f"Warning: Directory {directory} does not exist. Skipping...")
            continue
            
        conversion_summary[directory] = {
            'converted_files': [],
            'skipped_files': [],
            'errors': []
        }
        
        # Get all files in the directory
        files = glob.glob(os.path.join(directory, "*"))
        
        for file_path in files:
            if os.path.isfile(file_path):
                file_name = os.path.basename(file_path)
                file_ext = os.path.splitext(file_name)[1].lower()
                
                # Skip if already CSV
                if file_ext == '.csv':
                    conversion_summary[directory]['skipped_files'].append(file_name)
                    continue
                
                # Process non-CSV files
                if file_ext in ['.txt', '.dpt', '.dat', '.xls', '.xlsx']:
                    try:
                        # Try to read the file with different methods
                        data = None
                        
                        if file_ext in ['.txt', '.dpt', '.dat']:
                            data = pd.read_csv(file_path, delim_whitespace=True, header=None, encoding="latin-1", skiprows=2)
                        
                        elif file_ext in ['.xls', '.xlsx']:
                            data = pd.read_excel(file_path, header=None)
                        
                        if data is not None and len(data.columns) >= 2:
                            # Create new CSV filename
                            csv_filename = os.path.splitext(file_name)[0] + '.csv'
                            csv_path = os.path.join(directory, csv_filename)
                            
                            # Save as CSV
                            data.to_csv(csv_path, index=False, header=False)
                            
                            conversion_summary[directory]['converted_files'].append({
                                'original': file_name,
                                'converted': csv_filename
                            })
                            
                            print(f"Converted {file_name} to {csv_filename} in {directory}")
                        else:
                            conversion_summary[directory]['errors'].append(f"Could not parse {file_name} - insufficient columns")
                            
                    except Exception as e:
                        conversion_summary[directory]['errors'].append(f"Error converting {file_name}: {str(e)}")
                        print(f"Error converting {file_name}: {str(e)}")
                else:
                    conversion_summary[directory]['skipped_files'].append(file_name)
    
    # Print summary
    print("\n=== Conversion Summary ===")
    for directory, summary in conversion_summary.items():
        print(f"\nDirectory: {directory}")
        print(f"Converted files: {len(summary['converted_files'])}")
        print(f"Skipped files: {len(summary['skipped_files'])}")
        print(f"Errors: {len(summary['errors'])}")
        
        if summary['converted_files']:
            print("Converted files:")
            for file_info in summary['converted_files']:
                print(f"  {file_info['original']} -> {file_info['converted']}")
        if summary['errors']:
            print("Errors:")
            for error in summary['errors']:
                print(f"  {error}")
    
    return conversion_summary


# FUNCT2 Read data to extract relevant columns (in x-y = column 1-column 2 format), ensure float types and no NaNs.


# F4 Trim the data to remove data points that are outside the range of the x and y values given by the user in the argument. Return the data as a pandas dataframe x-y-values columns and a sample-ID column (ensure file extensions removed from sample names).


# FUNCT3 check for replicates using naming convention and take an average

# FUNCT4 Normalise data to 0-1 range for the y-values (column 2)

# FUNCT5 Interpolate data to N points between x-min and x-max

def trim_dataframe(df, x_min=None, x_max=None, y_min=None, y_max=None, x_col='X', y_col='Y', sample_col='sample'):
    """
    Trim a DataFrame by x and/or y value ranges.
    Args:
        df (pd.DataFrame): Input DataFrame with x, y, and sample columns.
        x_min (float, optional): Minimum x value to keep.
        x_max (float, optional): Maximum x value to keep.
        y_min (float, optional): Minimum y value to keep.
        y_max (float, optional): Maximum y value to keep.
        x_col (str): Name of the x column.
        y_col (str): Name of the y column.
        sample_col (str): Name of the sample ID column.
    Returns:
        pd.DataFrame: Trimmed DataFrame.
    """
    trimmed = df.copy()
    if x_min is not None:
        trimmed = trimmed[trimmed[x_col] >= x_min]
    if x_max is not None:
        trimmed = trimmed[trimmed[x_col] <= x_max]
    if y_min is not None:
        trimmed = trimmed[trimmed[y_col] >= y_min]
    if y_max is not None:
        trimmed = trimmed[trimmed[y_col] <= y_max]
    # Ensure sample_col is present and not lost
    if sample_col in trimmed.columns:
        trimmed[sample_col] = trimmed[sample_col]
    return trimmed
 