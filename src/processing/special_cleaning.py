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
    Normalize the y_col of the DataFrame to the 0-1 range, replacing the original column.
    Args:
        df (pd.DataFrame): Input DataFrame.
        y_col (str): Name of the y column to normalize.
    Returns:
        pd.DataFrame: DataFrame with y_col normalized to 0-1 range.
    """
    df = df.copy()
    y = df[y_col]
    df[y_col] = (y - y.min()) / (y.max() - y.min())
    return df

