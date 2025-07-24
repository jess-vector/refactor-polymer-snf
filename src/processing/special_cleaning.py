# special cleaning functions for specific data modalities

# TGA
import os
import pandas as pd

def tga_xy(tga_folder):
    """
    For each .csv file in the given TGA folder, extract and clean X and Y columns according to file type.
    Returns a list of cleaned DataFrames, one per file.
    """
    processed_dfs = []
    for fname in os.listdir(tga_folder):
        if fname.endswith('.csv'):
            file_path = os.path.join(tga_folder, fname)
            # Determine file type by prefix
            if fname.startswith("HDPE-"):
                # HDPE: skip 3 rows, X = col 1, Y = col 2
                df = pd.read_csv(file_path, skiprows=3, header=None, encoding="latin-1")
                if df.shape[1] < 3:
                    continue  # Not enough columns
                x = df.iloc[:, 1]
                y = df.iloc[:, 2]
            elif fname.startswith("LDPE-"):
                # LDPE: skip 3 rows, X = col 3, Y = col 2
                df = pd.read_csv(file_path, skiprows=3, header=None, encoding="latin-1")
                if df.shape[1] < 4:
                    continue  # Not enough columns
                x = df.iloc[:, 3]
                y = df.iloc[:, 2]
            else:
                continue  # Not a recognized TGA file

            # Convert to float and drop rows with non-numeric or NaN
            data = pd.DataFrame({
                'X': pd.to_numeric(x, errors='coerce'),
                'Y': pd.to_numeric(y, errors='coerce'),
            })
            data = data.dropna(subset=['X', 'Y'])
            data['sample'] = os.path.splitext(fname)[0]
            processed_dfs.append(data)
    return processed_dfs

def normalize_tga(df, y_col='Y'):
    """
    Normalize the y_col of the DataFrame so that the maximum value is 1, preserving residual mass.
    Args:
        df (pd.DataFrame): Input DataFrame.
        y_col (str): Name of the y column to normalize.
    Returns:
        pd.DataFrame: DataFrame with y_col normalized so max=1, preserving residual mass.
    """
    df = df.copy()
    y = df[y_col]
    max_y = y.max()
    df[y_col] = y / max_y
    return df

def dsc_xy(dsc_folder):
    """
    Process DSC .csv files in the given folder.
    For HDPE- files: already in X-Y format.
    For LDPE- files: skip 10 rows, X = col 1, Y = col 2 (after skip).
    Returns a list of cleaned DataFrames, one per file.
    """
    processed_dfs = []
    for fname in os.listdir(dsc_folder):
        if fname.endswith('.csv'):
            file_path = os.path.join(dsc_folder, fname)
            try:
                if fname.startswith("HDPE-"):
                    # HDPE: assume already in X-Y format, no skip
                    df = pd.read_csv(file_path, header=None, encoding="latin-1")
                    if df.empty or df.shape[1] < 2:
                        print(f"Warning: Skipping {fname} - insufficient data or columns")
                        continue  # Not enough columns
                    x = df.iloc[:, 0]
                    y = df.iloc[:, 1]
                elif fname.startswith("LDPE-"):
                    # LDPE: skip 10 rows, X = col 1, Y = col 2
                    df = pd.read_csv(file_path, skiprows=10, header=None, encoding="latin-1")
                    if df.empty or df.shape[1] < 3:
                        print(f"Warning: Skipping {fname} - insufficient data or columns")
                        continue  # Not enough columns
                    x = df.iloc[:, 1]
                    y = df.iloc[:, 2]
                else:
                    continue  # Not a recognized DSC file

                # Convert to float and drop rows with non-numeric or NaN
                data = pd.DataFrame({
                    'X': pd.to_numeric(x, errors='coerce'),
                    'Y': pd.to_numeric(y, errors='coerce'),
                })
                data = data.dropna(subset=['X', 'Y'])
                
                # Check if we have any valid data after cleaning
                if data.empty:
                    print(f"Warning: Skipping {fname} - no valid data after cleaning")
                    continue
                    
                data['sample'] = os.path.splitext(fname)[0]
                processed_dfs.append(data)
                print(f"Successfully processed: {fname}")
                
            except pd.errors.EmptyDataError:
                print(f"Warning: Skipping {fname} - file is empty or has no valid data")
                continue
            except Exception as e:
                print(f"Warning: Error processing {fname}: {str(e)}")
                continue
    return processed_dfs

