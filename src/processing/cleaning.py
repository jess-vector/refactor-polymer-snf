# Generic cleaning functions for all data modalities


# FUNCT1 check if data is in .csv format, if not convert to .csv function (if not already). All sample data is saved in a folder titled with relevant modality. 
import os
import pandas as pd
import glob
from pathlib import Path
import numpy as np

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

def select_trim(df, x_min=None, x_max=None, y_min=None, y_max=None, x_col='X', y_col='Y', sample_col='sample'):
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

 
def auto_trim(dfs, x_col='X'):
    """
    Automatically trims a list of DataFrames to the overlapping x range.
    Finds the maximum of all minimum x values and the minimum of all maximum x values,
    then trims each DataFrame to this range.

    Args:
        dfs (list of pd.DataFrame): List of DataFrames, each with an x_col.
        x_col (str): Name of the x column.

    Returns:
        list of pd.DataFrame: List of trimmed DataFrames.
    """
    # Find the min and max x for each DataFrame
    min_xs = []
    max_xs = []
    for df in dfs:
        if not df.empty:
            min_xs.append(df[x_col].min())
            max_xs.append(df[x_col].max())
    if not min_xs or not max_xs:
        return dfs  # Return as is if no data

    overlap_min = max(min_xs)
    overlap_max = min(max_xs)

    trimmed_dfs = []
    for df in dfs:
        trimmed = df[(df[x_col] >= overlap_min) & (df[x_col] <= overlap_max)].copy()
        trimmed_dfs.append(trimmed)
    return trimmed_dfs



def interprolate_data(dfs, x_col='X', y_col='Y', N=3000):
    """
    Interpolates each DataFrame's y_col to N points over the common x range.
    Returns a 2D NumPy array: shape (num_samples, N), each row is a sample's interpolated y-values.

    Args:
        dfs (list of pd.DataFrame): List of DataFrames to interpolate.
        x_col (str): Name of the x column.
        y_col (str): Name of the y column.
        N (int): Number of points to interpolate to (default 3000).

    Returns:
        np.ndarray: 2D array of shape (num_samples, N) with interpolated y-values.
    """
    # Find overlapping x range
    min_xs = []
    max_xs = []
    for df in dfs:
        if not df.empty:
            min_xs.append(df[x_col].min())
            max_xs.append(df[x_col].max())
    if not min_xs or not max_xs:
        raise ValueError("No valid dataframes with data to interpolate.")

    overlap_min = max(min_xs)
    overlap_max = min(max_xs)
    if overlap_max <= overlap_min:
        raise ValueError("No overlapping x range found for interpolation.")

    x_new = np.linspace(overlap_min, overlap_max, N)
    interpolated = []

    for df in dfs:
        # Drop duplicates and sort by x_col
        df_sorted = df.drop_duplicates(subset=x_col).sort_values(by=x_col)
        x = df_sorted[x_col].values
        y = df_sorted[y_col].values
        # Only use points within the overlap range
        mask = (x >= overlap_min) & (x <= overlap_max)
        x = x[mask]
        y = y[mask]
        if len(x) < 2:
            # Not enough points to interpolate, fill with NaN
            interpolated.append(np.full(N, np.nan))
            continue
        y_interp = np.interp(x_new, x, y)
        interpolated.append(y_interp)
    return np.vstack(interpolated)
