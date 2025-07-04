# processing module

# cleaning/__init__.py
"""
This module provides data cleaning and processing functions for all data modalities.
Each function is implemented in its respective file for modularity.
"""

# Import all cleaning functions from the modules
from .cleaning import convert_csv
from .special_cleaning import tga_xy
from .cleaning import trim_dataframe
from .special_cleaning import normalize_tga
# Add all functions to __all__
__all__ = [
    "convert_csv",
    "tga_xy",
    "trim_dataframe",
    "normalize_tga",
]