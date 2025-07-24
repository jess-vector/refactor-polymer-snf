# Processed Data Documentation

This directory contains the processed and interpolated TGA and DSC data organized into separate folders.

## Directory Structure

```
processed_data/
├── tga/                    # TGA (Thermogravimetric Analysis) data
│   ├── interpolated_tga_data.npy      # Main interpolated data array
│   ├── tga_metadata.npz               # Metadata about the data
│   ├── tga_sample_names.txt           # Sample names in order
│   └── tga_sample_index_mapping.txt   # Index to sample name mapping
└── dsc/                    # DSC (Differential Scanning Calorimetry) data
    ├── interpolated_dsc_data.npy      # Main interpolated data array
    ├── dsc_metadata.npz               # Metadata about the data
    ├── dsc_sample_names.txt           # Sample names in order
    └── dsc_sample_index_mapping.txt   # Index to sample name mapping
```

## Data Format

### TGA Data (`tga/interpolated_tga_data.npy`)
- **Shape**: `(num_samples, 3000)`
- **Data type**: `float64`
- **Content**: Normalized mass loss data interpolated to 3000 points
- **Temperature range**: Automatically determined from overlapping range across all samples
- **Normalization**: Mass-normalized (0-1 scale)

### DSC Data (`dsc/interpolated_dsc_data.npy`)
- **Shape**: `(num_samples, 3000)`
- **Data type**: `float64`
- **Content**: Heat flow data interpolated to 3000 points
- **Temperature range**: 60-180°C (trimmed range)
- **Units**: W/g

## Metadata Files

### TGA Metadata (`tga/tga_metadata.npz`)
Contains:
- `num_samples`: Number of samples
- `num_points`: Number of interpolation points (3000)
- `x_range`: Temperature range [min, max]
- `sample_names`: List of sample names
- `data_type`: "TGA"
- `normalization`: "mass_normalized"
- `interpolation_points`: 3000

### DSC Metadata (`dsc/dsc_metadata.npz`)
Contains:
- `num_samples`: Number of samples
- `num_points`: Number of interpolation points (3000)
- `x_range`: Temperature range [min, max]
- `sample_names`: List of sample names
- `data_type`: "DSC"
- `trim_range`: [60, 180] (temperature range used for trimming)
- `interpolation_points`: 3000

## Usage Examples

### Loading TGA Data
```python
import numpy as np

# Load the interpolated data
tga_data = np.load("processed_data/tga/interpolated_tga_data.npy")

# Load metadata
metadata = np.load("processed_data/tga/tga_metadata.npz", allow_pickle=True)

# Load sample names
with open("processed_data/tga/tga_sample_names.txt", 'r') as f:
    sample_names = [line.strip().split(': ')[1] for line in f.readlines()]

print(f"TGA data shape: {tga_data.shape}")
print(f"Number of samples: {len(sample_names)}")
print(f"Temperature range: {metadata['x_range'][0]:.1f}°C to {metadata['x_range'][1]:.1f}°C")
```

### Loading DSC Data
```python
import numpy as np

# Load the interpolated data
dsc_data = np.load("processed_data/dsc/interpolated_dsc_data.npy")

# Load metadata
metadata = np.load("processed_data/dsc/dsc_metadata.npz", allow_pickle=True)

# Load sample names
with open("processed_data/dsc/dsc_sample_names.txt", 'r') as f:
    sample_names = [line.strip().split(': ')[1] for line in f.readlines()]

print(f"DSC data shape: {dsc_data.shape}")
print(f"Number of samples: {len(sample_names)}")
print(f"Temperature range: {metadata['x_range'][0]:.1f}°C to {metadata['x_range'][1]:.1f}°C")
```

### Plotting Data
```python
import matplotlib.pyplot as np

# For TGA data
x_tga = np.linspace(metadata['x_range'][0], metadata['x_range'][1], tga_data.shape[1])
for i, sample_name in enumerate(sample_names):
    plt.plot(x_tga, tga_data[i], label=sample_name)

plt.xlabel('Temperature (°C)')
plt.ylabel('Normalized Mass')
plt.title('TGA Data')
plt.legend()
plt.show()
```

## Data Processing Steps

1. **Raw Data Loading**: Original CSV files from TGA and DSC instruments
2. **Cleaning**: Removal of headers, conversion to proper format
3. **Trimming**: 
   - TGA: Automatic trimming to find overlapping temperature range
   - DSC: Manual trimming to 60-180°C range
4. **Normalization**: 
   - TGA: Mass normalization (0-1 scale)
   - DSC: No normalization (raw heat flow values)
5. **Interpolation**: All curves interpolated to 3000 points for consistent analysis
6. **Saving**: Data saved in organized structure with metadata

## Notes

- All data is interpolated to the same number of points (3000) for consistent analysis
- Sample names are preserved in the order they appear in the data arrays
- The temperature axis can be reconstructed using the metadata's `x_range`
- Both TGA and DSC data are ready for machine learning or statistical analysis 