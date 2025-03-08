"""
pubmed_scrapper package

This module fetches and processes research papers from PubMed.
"""

# Import key functions for easy access
from .fetcher import fetch_pubmed_data
from .parser import extract_relevant_data

# Define the package version
__version__ = "0.1.0"

# Expose key functions when doing `from pubmed_scrapper import *`
__all__ = ["fetch_pubmed_data", "extract_relevant_data", "__version__"]
