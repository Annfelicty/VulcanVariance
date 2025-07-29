#!/usr/bin/env python3
"""
Script to create comprehensive EDA notebook for movie analysis project.
"""

import json
from pathlib import Path

def create_eda_notebook():
    """Create the comprehensive EDA notebook."""
    
    notebook = {
        "cells": [
            # Title and introduction
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Movie Industry Exploratory Data Analysis\n",
                    "## Comprehensive Analysis of Movie Performance, Ratings, and Financial Data\n",
                    "\n",
                    "This notebook performs thorough exploratory data analysis on cleaned movie datasets to uncover insights about:\n",
                    "\n",
                    "### 🎯 Analysis Objectives:\n",
                    "- **Movie Performance Trends** - Box office performance over time\n",
                    "- **Rating Patterns** - TMDb and Rotten Tomatoes rating distributions\n",
                    "- **Financial Analysis** - Budget vs revenue relationships\n",
                    "- **Genre Analysis** - Popular genres and their performance\n",
                    "- **Studio Analysis** - Top performing studios and distributors\n",
                    "- **Temporal Trends** - Movie industry evolution over years\n",
                    "\n",
                    "### 📋 Cleaned Datasets Used:\n",
                    "- **TMDb Movies** (26,517 records) - Movie metadata, ratings, popularity\n",
                    "- **Movie Budgets** (5,782 records) - Production budgets and revenues\n",
                    "- **Box Office Mojo** (3,387 records) - Domestic and foreign gross earnings\n",
                    "- **Rotten Tomatoes** (1,560 records) - Critical ratings and movie info"
                ]
            },
            
            # Setup and imports
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Import required libraries for comprehensive EDA\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "import plotly.express as px\n",
                    "import plotly.graph_objects as go\n",
                    "from plotly.subplots import make_subplots\n",
                    "import warnings\n",
                    "from pathlib import Path\n",
                    "from datetime import datetime\n",
                    "import re\n",
                    "\n",
                    "# Configure visualization settings\n",
                    "plt.style.use('seaborn-v0_8')\n",
                    "sns.set_palette(\"husl\")\n",
                    "plt.rcParams['figure.figsize'] = (12, 8)\n",
                    "pd.set_option('display.max_columns', None)\n",
                    "warnings.filterwarnings('ignore')\n",
                    "\n",
                    "print(\"✅ Libraries imported successfully!\")\n",
                    "print(f\"📊 Analysis environment ready\")"
                ]
            },
            
            # Data loading section
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Data Loading and Initial Overview\n",
                    "\n",
                    "Loading all cleaned datasets and performing initial data quality checks."
                ]
            },
            
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Load all cleaned datasets\n",
                    "print(\"📂 Loading cleaned datasets...\")\n",
                    "print(\"=\" * 40)\n",
                    "\n",
                    "# Load datasets\n",
                    "tmdb_df = pd.read_csv('cleaned_data/tmdb_movies_cleaned.csv')\n",
                    "budgets_df = pd.read_csv('cleaned_data/movie_budgets_cleaned.csv')\n",
                    "bom_df = pd.read_csv('cleaned_data/box_office_mojo_cleaned.csv')\n",
                    "rt_df = pd.read_csv('cleaned_data/rotten_tomatoes_info_cleaned.csv')\n",
                    "\n",
                    "# Convert date columns\n",
                    "tmdb_df['release_date'] = pd.to_datetime(tmdb_df['release_date'])\n",
                    "budgets_df['release_date'] = pd.to_datetime(budgets_df['release_date'])\n",
                    "\n",
                    "datasets = {\n",
                    "    'TMDb Movies': tmdb_df,\n",
                    "    'Movie Budgets': budgets_df,\n",
                    "    'Box Office Mojo': bom_df,\n",
                    "    'Rotten Tomatoes': rt_df\n",
                    "}\n",
                    "\n",
                    "# Display basic info for each dataset\n",
                    "for name, df in datasets.items():\n",
                    "    print(f\"\\n📊 {name}:\")\n",
                    "    print(f\"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns\")\n",
                    "    print(f\"   Columns: {list(df.columns)}\")\n",
                    "    print(f\"   Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB\")\n",
                    "\n",
                    "print(\"\\n✅ All datasets loaded successfully!\")"
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

# Create and save the EDA notebook
eda_notebook = create_eda_notebook()

with open('notebooks/02_exploratory_data_analysis.ipynb', 'w') as f:
    json.dump(eda_notebook, f, indent=2)

print("✅ Created comprehensive EDA notebook structure!")