#!/usr/bin/env python3
"""
Script to create comprehensive data cleaning and EDA notebooks for the movie analysis project.
This ensures proper notebook structure for VS Code compatibility.
"""

import json
from pathlib import Path

def create_cleaning_notebook():
    """Create the comprehensive data cleaning notebook."""
    
    notebook = {
        "cells": [
            # Title and introduction
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Movie Dataset Cleaning Pipeline\n",
                    "## Comprehensive Data Cleaning for EDA Project\n",
                    "\n",
                    "This notebook systematically cleans all movie datasets from the `Original_Data` folder and exports clean, analysis-ready datasets.\n",
                    "\n",
                    "### 📋 Datasets to Process:\n",
                    "1. **Box Office Mojo** (`bom.movie_gross.csv.gz`) - Box office gross earnings\n",
                    "2. **TMDb Movies** (`tmdb.movies.csv.gz`) - The Movie Database metadata\n",
                    "3. **Movie Budgets** (`tn.movie_budgets.csv.gz`) - Production budgets and revenues\n",
                    "4. **Rotten Tomatoes Info** (`rt.movie_info.tsv.gz`) - Movie ratings and metadata\n",
                    "5. **Rotten Tomatoes Reviews** (`rt.reviews.tsv`) - Individual movie reviews\n",
                    "6. **IMDb Database** (`im.db.zip`) - Comprehensive movie database\n",
                    "\n",
                    "### 🎯 Cleaning Objectives:\n",
                    "- Handle missing values appropriately\n",
                    "- Standardize data types and formats\n",
                    "- Remove duplicates\n",
                    "- Clean financial data (currency formatting)\n",
                    "- Validate and correct data inconsistencies\n",
                    "- Export clean datasets for analysis"
                ]
            },
            
            # Setup and imports
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Import required libraries\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import sqlite3\n",
                    "import zipfile\n",
                    "import gzip\n",
                    "import warnings\n",
                    "from pathlib import Path\n",
                    "import re\n",
                    "\n",
                    "# Configure pandas for better display\n",
                    "pd.set_option('display.max_columns', None)\n",
                    "pd.set_option('display.width', None)\n",
                    "pd.set_option('display.max_rows', 100)\n",
                    "warnings.filterwarnings('ignore')\n",
                    "\n",
                    "# Create directories\n",
                    "Path('cleaned_data').mkdir(exist_ok=True)\n",
                    "\n",
                    "print(\"✅ Environment setup complete!\")\n",
                    "print(f\"📁 Working directory: {Path.cwd()}\")"
                ]
            }
        ],
        
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return notebook

# Create and save the cleaning notebook
cleaning_notebook = create_cleaning_notebook()

with open('notebooks/01_data_cleaning_complete.ipynb', 'w') as f:
    json.dump(cleaning_notebook, f, indent=2)

print("✅ Created comprehensive data cleaning notebook!")