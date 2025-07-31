# processing module

# cleaning/__init__.py
"""
This module provides data cleaning and processing functions for all data modalities.
Each function is implemented in its respective file for modularity.
"""

# Import all cleaning functions from the modules
from .cleaning import convert_csv, auto_trim, select_trim, interprolate_data
from .special_cleaning import tga_xy, normalize_tga, dsc_xy, avg_ftir
# Add all functions to __all__
__all__ = [
    "convert_csv",
    "tga_xy",
    "select_trim",
    "normalize_tga",
    "auto_trim",
    "interprolate_data",
    "dsc_xy",
    "avg_ftir",
]