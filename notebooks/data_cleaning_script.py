#!/usr/bin/env python3
"""
Movie Dataset EDA - Data Cleaning Script

This script cleans and prepares multiple movie datasets for exploratory data analysis.
We'll process all datasets from the Original_Data folder and save cleaned versions.

Author: Data Science Team
Date: 2024
"""

# Import necessary libraries for data cleaning and analysis
# We import these specific libraries because:
# - pandas: Essential for data manipulation and analysis
# - numpy: Provides numerical computing capabilities  
# - matplotlib/seaborn: For data visualization during cleaning process
# - sqlite3: To handle the IMDb database
# - zipfile/gzip: To extract compressed data files
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import zipfile
import gzip
import os
import warnings
from pathlib import Path

# Configure pandas display options for better data inspection
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
warnings.filterwarnings('ignore')

# Set up plotting style for consistent visualizations
plt.style.use('default')
sns.set_palette("husl")

print("="*60)
print("🎬 MOVIE DATASET CLEANING PIPELINE")
print("="*60)
print("✅ Libraries imported successfully!")
print(f"📊 Pandas version: {pd.__version__}")
print(f"🔢 NumPy version: {np.__version__}")

# Define file paths
original_data_path = Path('Original_Data')
cleaned_data_path = Path('Cleaned_Data')

# Create cleaned data directory if it doesn't exist
cleaned_data_path.mkdir(exist_ok=True)

print(f"\n📁 Data directories:")
print(f"   Original: {original_data_path}")
print(f"   Cleaned:  {cleaned_data_path}")

def inspect_dataset_files():
    """
    Inspect all files in the original data directory
    This helps us understand what we're working with before cleaning
    """
    print("\n" + "="*50)
    print("📋 DATASET INVENTORY")
    print("="*50)
    
    files_info = []
    for file_path in original_data_path.iterdir():
        if file_path.is_file():
            size_mb = file_path.stat().st_size / (1024 * 1024)  # Convert to MB
            files_info.append({
                'filename': file_path.name,
                'size_mb': round(size_mb, 2),
                'extension': file_path.suffix
            })
    
    # Create and display summary
    files_df = pd.DataFrame(files_info)
    files_df = files_df.sort_values('size_mb', ascending=False)
    
    print(files_df.to_string(index=False))
    print(f"\n📊 Total files: {len(files_df)}")
    print(f"💾 Total size: {files_df['size_mb'].sum():.2f} MB")
    return files_df

def clean_box_office_data():
    """
    Clean Box Office Mojo dataset (bom.movie_gross.csv.gz)
    This dataset contains movie box office performance data
    """
    print("\n" + "="*50)
    print("🎬 CLEANING: Box Office Mojo Data")
    print("="*50)
    
    # Load the dataset
    # We use compression='gzip' to automatically handle the .gz file
    print("📥 Loading bom.movie_gross.csv.gz...")
    bom_df = pd.read_csv(original_data_path / 'bom.movie_gross.csv.gz', compression='gzip')
    
    print(f"✅ Loaded {len(bom_df)} records with {len(bom_df.columns)} columns")
    print(f"📋 Columns: {list(bom_df.columns)}")
    
    # Inspect data quality
    print("\n🔍 Data Quality Assessment:")
    print(f"   Shape: {bom_df.shape}")
    print(f"   Memory usage: {bom_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Check for missing values
    missing_data = bom_df.isnull().sum()
    print("\n❌ Missing Values:")
    for col in bom_df.columns:
        missing_count = missing_data[col]
        missing_percent = (missing_count / len(bom_df)) * 100
        status = "✅ Clean" if missing_count == 0 else f"❌ {missing_count} ({missing_percent:.1f}%)"
        print(f"   {col}: {status}")
    
    # Check for duplicates
    duplicates = bom_df.duplicated().sum()
    print(f"\n🔄 Duplicate rows: {duplicates}")
    
    # Show sample data
    print("\n👀 Sample data:")
    print(bom_df.head(3))
    
    # Start cleaning process
    print("\n🧹 Cleaning Process:")
    bom_clean = bom_df.copy()
    
    # Remove duplicates if any
    if duplicates > 0:
        bom_clean = bom_clean.drop_duplicates()
        print(f"   🗑️  Removed {duplicates} duplicate rows")
    
    # Clean monetary columns (remove currency symbols, convert to numeric)
    money_columns = [col for col in bom_clean.columns if any(x in col.lower() for x in ['gross', 'revenue', 'budget', 'sales'])]
    for col in money_columns:
        if bom_clean[col].dtype == 'object':
            # Remove currency symbols and commas, convert to numeric
            bom_clean[col] = bom_clean[col].astype(str).str.replace(r'[$,]', '', regex=True)
            bom_clean[col] = pd.to_numeric(bom_clean[col], errors='coerce')
            print(f"   💰 Cleaned monetary column: {col}")
    
    # Clean year columns
    year_columns = [col for col in bom_clean.columns if 'year' in col.lower()]
    for col in year_columns:
        bom_clean[col] = pd.to_numeric(bom_clean[col], errors='coerce')
        print(f"   📅 Cleaned year column: {col}")
    
    # Clean text columns (strip whitespace, handle nulls)
    text_columns = bom_clean.select_dtypes(include=['object']).columns
    for col in text_columns:
        if col not in money_columns:
            bom_clean[col] = bom_clean[col].astype(str).str.strip()
            bom_clean[col] = bom_clean[col].replace('nan', np.nan)  # Convert 'nan' strings back to NaN
            print(f"   📝 Cleaned text column: {col}")
    
    # Save cleaned dataset
    output_file = cleaned_data_path / 'bom_movie_gross_cleaned.csv'
    bom_clean.to_csv(output_file, index=False)
    print(f"\n💾 Saved cleaned data to: {output_file}")
    print(f"✅ Final shape: {bom_clean.shape}")
    
    return bom_clean

def clean_movie_budgets_data():
    """
    Clean The Numbers movie budgets dataset (tn.movie_budgets.csv.gz)
    This dataset contains movie budget and revenue information
    """
    print("\n" + "="*50)
    print("💰 CLEANING: Movie Budgets Data")
    print("="*50)
    
    print("📥 Loading tn.movie_budgets.csv.gz...")
    budgets_df = pd.read_csv(original_data_path / 'tn.movie_budgets.csv.gz', compression='gzip')
    
    print(f"✅ Loaded {len(budgets_df)} records with {len(budgets_df.columns)} columns")
    print(f"📋 Columns: {list(budgets_df.columns)}")
    
    # Data quality assessment
    print("\n🔍 Data Quality Assessment:")
    missing_data = budgets_df.isnull().sum()
    for col in budgets_df.columns:
        missing_count = missing_data[col]
        missing_percent = (missing_count / len(budgets_df)) * 100
        status = "✅ Clean" if missing_count == 0 else f"❌ {missing_count} ({missing_percent:.1f}%)"
        print(f"   {col}: {status}")
    
    print(f"\n🔄 Duplicate rows: {budgets_df.duplicated().sum()}")
    print("\n👀 Sample data:")
    print(budgets_df.head(3))
    
    # Cleaning process
    print("\n🧹 Cleaning Process:")
    budgets_clean = budgets_df.copy()
    
    # Remove duplicates
    budgets_clean = budgets_clean.drop_duplicates()
    
    # Clean monetary columns more thoroughly
    money_columns = [col for col in budgets_clean.columns if any(x in col.lower() for x in ['budget', 'gross', 'revenue'])]
    for col in money_columns:
        if budgets_clean[col].dtype == 'object':
            # Remove currency symbols, commas, and handle various formats
            budgets_clean[col] = budgets_clean[col].astype(str).str.replace(r'[$,]', '', regex=True)
            budgets_clean[col] = pd.to_numeric(budgets_clean[col], errors='coerce')
            print(f"   💰 Cleaned monetary column: {col}")
    
    # Clean release date if present
    date_columns = [col for col in budgets_clean.columns if any(x in col.lower() for x in ['date', 'release'])]
    for col in date_columns:
        try:
            budgets_clean[col] = pd.to_datetime(budgets_clean[col], errors='coerce')
            print(f"   📅 Cleaned date column: {col}")
        except:
            print(f"   ⚠️  Could not parse dates in column: {col}")
    
    # Clean text columns
    text_columns = budgets_clean.select_dtypes(include=['object']).columns
    for col in text_columns:
        if col not in money_columns and col not in date_columns:
            budgets_clean[col] = budgets_clean[col].astype(str).str.strip()
            budgets_clean[col] = budgets_clean[col].replace('nan', np.nan)
            print(f"   📝 Cleaned text column: {col}")
    
    # Save cleaned dataset
    output_file = cleaned_data_path / 'movie_budgets_cleaned.csv'
    budgets_clean.to_csv(output_file, index=False)
    print(f"\n💾 Saved cleaned data to: {output_file}")
    print(f"✅ Final shape: {budgets_clean.shape}")
    
    return budgets_clean

def clean_tmdb_data():
    """
    Clean The Movie Database (TMDb) dataset (tmdb.movies.csv.gz)
    This dataset contains comprehensive movie information from TMDb
    """
    print("\n" + "="*50)
    print("🎭 CLEANING: TMDb Movies Data")
    print("="*50)
    
    print("📥 Loading tmdb.movies.csv.gz...")
    tmdb_df = pd.read_csv(original_data_path / 'tmdb.movies.csv.gz', compression='gzip')
    
    print(f"✅ Loaded {len(tmdb_df)} records with {len(tmdb_df.columns)} columns")
    print(f"📋 Columns: {list(tmdb_df.columns)}")
    
    # Data quality assessment
    print("\n🔍 Data Quality Assessment:")
    missing_data = tmdb_df.isnull().sum()
    for col in tmdb_df.columns:
        missing_count = missing_data[col]
        missing_percent = (missing_count / len(tmdb_df)) * 100
        status = "✅ Clean" if missing_count == 0 else f"❌ {missing_count} ({missing_percent:.1f}%)"
        print(f"   {col}: {status}")
    
    print(f"\n🔄 Duplicate rows: {tmdb_df.duplicated().sum()}")
    print("\n👀 Sample data:")
    print(tmdb_df.head(3))
    
    # Cleaning process
    print("\n🧹 Cleaning Process:")
    tmdb_clean = tmdb_df.copy()
    
    # Remove duplicates
    tmdb_clean = tmdb_clean.drop_duplicates()
    
    # Clean numeric columns (budget, revenue, runtime, etc.)
    numeric_columns = [col for col in tmdb_clean.columns if any(x in col.lower() for x in ['budget', 'revenue', 'runtime', 'vote_average', 'vote_count', 'popularity'])]
    for col in numeric_columns:
        if col in tmdb_clean.columns:
            tmdb_clean[col] = pd.to_numeric(tmdb_clean[col], errors='coerce')
            print(f"   🔢 Cleaned numeric column: {col}")
    
    # Clean date columns
    date_columns = [col for col in tmdb_clean.columns if any(x in col.lower() for x in ['date', 'release'])]
    for col in date_columns:
        try:
            tmdb_clean[col] = pd.to_datetime(tmdb_clean[col], errors='coerce')
            print(f"   📅 Cleaned date column: {col}")
        except:
            print(f"   ⚠️  Could not parse dates in column: {col}")
    
    # Clean text columns and handle JSON-like columns (genres, keywords, etc.)
    text_columns = tmdb_clean.select_dtypes(include=['object']).columns
    for col in text_columns:
        if col not in date_columns:
            tmdb_clean[col] = tmdb_clean[col].astype(str).str.strip()
            tmdb_clean[col] = tmdb_clean[col].replace('nan', np.nan)
            print(f"   📝 Cleaned text column: {col}")
    
    # Save cleaned dataset
    output_file = cleaned_data_path / 'tmdb_movies_cleaned.csv'
    tmdb_clean.to_csv(output_file, index=False)
    print(f"\n💾 Saved cleaned data to: {output_file}")
    print(f"✅ Final shape: {tmdb_clean.shape}")
    
    return tmdb_clean

def clean_rotten_tomatoes_info():
    """
    Clean Rotten Tomatoes movie info dataset (rt.movie_info.tsv.gz)
    This dataset contains movie information from Rotten Tomatoes
    """
    print("\n" + "="*50)
    print("🍅 CLEANING: Rotten Tomatoes Movie Info")
    print("="*50)
    
    print("📥 Loading rt.movie_info.tsv.gz...")
    # Note: This is a TSV file, so we use sep='\t'
    rt_info_df = pd.read_csv(original_data_path / 'rt.movie_info.tsv.gz', 
                           compression='gzip', sep='\t')
    
    print(f"✅ Loaded {len(rt_info_df)} records with {len(rt_info_df.columns)} columns")
    print(f"📋 Columns: {list(rt_info_df.columns)}")
    
    # Data quality assessment
    print("\n🔍 Data Quality Assessment:")
    missing_data = rt_info_df.isnull().sum()
    for col in rt_info_df.columns:
        missing_count = missing_data[col]
        missing_percent = (missing_count / len(rt_info_df)) * 100
        status = "✅ Clean" if missing_count == 0 else f"❌ {missing_count} ({missing_percent:.1f}%)"
        print(f"   {col}: {status}")
    
    print(f"\n🔄 Duplicate rows: {rt_info_df.duplicated().sum()}")
    print("\n👀 Sample data:")
    print(rt_info_df.head(3))
    
    # Cleaning process
    print("\n🧹 Cleaning Process:")
    rt_info_clean = rt_info_df.copy()
    
    # Remove duplicates
    rt_info_clean = rt_info_clean.drop_duplicates()
    
    # Clean rating/score columns
    rating_columns = [col for col in rt_info_clean.columns if any(x in col.lower() for x in ['rating', 'score', 'percent'])]
    for col in rating_columns:
        if col in rt_info_clean.columns:
            # Remove percentage signs and convert to numeric
            if rt_info_clean[col].dtype == 'object':
                rt_info_clean[col] = rt_info_clean[col].astype(str).str.replace('%', '')
                rt_info_clean[col] = pd.to_numeric(rt_info_clean[col], errors='coerce')
            print(f"   ⭐ Cleaned rating column: {col}")
    
    # Clean year columns
    year_columns = [col for col in rt_info_clean.columns if 'year' in col.lower()]
    for col in year_columns:
        rt_info_clean[col] = pd.to_numeric(rt_info_clean[col], errors='coerce')
        print(f"   📅 Cleaned year column: {col}")
    
    # Clean text columns
    text_columns = rt_info_clean.select_dtypes(include=['object']).columns
    for col in text_columns:
        if col not in rating_columns:
            rt_info_clean[col] = rt_info_clean[col].astype(str).str.strip()
            rt_info_clean[col] = rt_info_clean[col].replace('nan', np.nan)
            print(f"   📝 Cleaned text column: {col}")
    
    # Save cleaned dataset
    output_file = cleaned_data_path / 'rt_movie_info_cleaned.csv'
    rt_info_clean.to_csv(output_file, index=False)
    print(f"\n💾 Saved cleaned data to: {output_file}")
    print(f"✅ Final shape: {rt_info_clean.shape}")
    
    return rt_info_clean

def clean_rotten_tomatoes_reviews():
    """
    Clean Rotten Tomatoes reviews dataset (rt.reviews.tsv)
    This dataset contains individual movie reviews from Rotten Tomatoes
    """
    print("\n" + "="*50)
    print("📝 CLEANING: Rotten Tomatoes Reviews")
    print("="*50)
    
    print("📥 Loading rt.reviews.tsv...")
    # This file is not compressed
    rt_reviews_df = pd.read_csv(original_data_path / 'rt.reviews.tsv', sep='\t')
    
    print(f"✅ Loaded {len(rt_reviews_df)} records with {len(rt_reviews_df.columns)} columns")
    print(f"📋 Columns: {list(rt_reviews_df.columns)}")
    
    # Data quality assessment
    print("\n🔍 Data Quality Assessment:")
    missing_data = rt_reviews_df.isnull().sum()
    for col in rt_reviews_df.columns:
        missing_count = missing_data[col]
        missing_percent = (missing_count / len(rt_reviews_df)) * 100
        status = "✅ Clean" if missing_count == 0 else f"❌ {missing_count} ({missing_percent:.1f}%)"
        print(f"   {col}: {status}")
    
    print(f"\n🔄 Duplicate rows: {rt_reviews_df.duplicated().sum()}")
    print("\n👀 Sample data:")
    print(rt_reviews_df.head(3))
    
    # Cleaning process
    print("\n🧹 Cleaning Process:")
    rt_reviews_clean = rt_reviews_df.copy()
    
    # Remove duplicates
    rt_reviews_clean = rt_reviews_clean.drop_duplicates()
    
    # Clean rating columns
    rating_columns = [col for col in rt_reviews_clean.columns if any(x in col.lower() for x in ['rating', 'score'])]
    for col in rating_columns:
        if col in rt_reviews_clean.columns:
            rt_reviews_clean[col] = pd.to_numeric(rt_reviews_clean[col], errors='coerce')
            print(f"   ⭐ Cleaned rating column: {col}")
    
    # Clean date columns
    date_columns = [col for col in rt_reviews_clean.columns if any(x in col.lower() for x in ['date'])]
    for col in date_columns:
        try:
            rt_reviews_clean[col] = pd.to_datetime(rt_reviews_clean[col], errors='coerce')
            print(f"   📅 Cleaned date column: {col}")
        except:
            print(f"   ⚠️  Could not parse dates in column: {col}")
    
    # Clean text columns (reviews, critic names, etc.)
    text_columns = rt_reviews_clean.select_dtypes(include=['object']).columns
    for col in text_columns:
        if col not in date_columns:
            rt_reviews_clean[col] = rt_reviews_clean[col].astype(str).str.strip()
            rt_reviews_clean[col] = rt_reviews_clean[col].replace('nan', np.nan)
            print(f"   📝 Cleaned text column: {col}")
    
    # Save cleaned dataset
    output_file = cleaned_data_path / 'rt_reviews_cleaned.csv'
    rt_reviews_clean.to_csv(output_file, index=False)
    print(f"\n💾 Saved cleaned data to: {output_file}")
    print(f"✅ Final shape: {rt_reviews_clean.shape}")
    
    return rt_reviews_clean

def extract_and_clean_imdb_data():
    """
    Extract and clean IMDb database (im.db.zip)
    This is a SQLite database containing comprehensive movie data
    """
    print("\n" + "="*50)
    print("🎪 CLEANING: IMDb Database")
    print("="*50)
    
    # First, extract the zip file
    zip_path = original_data_path / 'im.db.zip'
    extract_path = original_data_path / 'extracted'
    extract_path.mkdir(exist_ok=True)
    
    print("📦 Extracting im.db.zip...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # Find the database file
    db_files = list(extract_path.glob('*.db'))
    if not db_files:
        print("❌ No .db file found in the extracted archive")
        return None
    
    db_path = db_files[0]
    print(f"✅ Found database: {db_path}")
    
    # Connect to the database and explore its structure
    print("\n🔍 Exploring database structure...")
    conn = sqlite3.connect(db_path)
    
    # Get list of tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"📊 Found {len(tables)} tables:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   {table_name}: {count:,} records")
    
    # Extract and clean each table
    cleaned_tables = {}
    for table in tables:
        table_name = table[0]
        print(f"\n🧹 Cleaning table: {table_name}")
        
        # Load table into pandas
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        print(f"   📥 Loaded {len(df)} records with {len(df.columns)} columns")
        
        # Basic cleaning
        df_clean = df.copy()
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        # Clean text columns
        text_columns = df_clean.select_dtypes(include=['object']).columns
        for col in text_columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace('nan', np.nan)
        
        # Convert numeric columns
        for col in df_clean.columns:
            if col not in text_columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Save cleaned table
        output_file = cleaned_data_path / f'imdb_{table_name}_cleaned.csv'
        df_clean.to_csv(output_file, index=False)
        print(f"   💾 Saved to: {output_file}")
        
        cleaned_tables[table_name] = df_clean
    
    conn.close()
    print(f"\n✅ Processed {len(cleaned_tables)} IMDb tables")
    
    return cleaned_tables

def generate_cleaning_summary():
    """
    Generate a summary report of the cleaning process
    """
    print("\n" + "="*60)
    print("📋 CLEANING SUMMARY REPORT")
    print("="*60)
    
    # List all cleaned files
    cleaned_files = list(cleaned_data_path.glob('*.csv'))
    
    print(f"📁 Cleaned datasets saved to: {cleaned_data_path}")
    print(f"📊 Total cleaned files: {len(cleaned_files)}")
    print("\n📄 Cleaned datasets:")
    
    total_size = 0
    for file_path in sorted(cleaned_files):
        size_mb = file_path.stat().st_size / (1024 * 1024)
        total_size += size_mb
        
        # Get basic info about each file
        try:
            df = pd.read_csv(file_path, nrows=1)  # Just read header
            cols = len(df.columns)
            
            # Get actual row count
            with open(file_path, 'r') as f:
                rows = sum(1 for line in f) - 1  # Subtract header
                
            print(f"   📄 {file_path.name}")
            print(f"      📊 {rows:,} rows × {cols} columns")
            print(f"      💾 {size_mb:.2f} MB")
        except:
            print(f"   📄 {file_path.name} ({size_mb:.2f} MB)")
    
    print(f"\n💾 Total size of cleaned data: {total_size:.2f} MB")
    
    # Cleaning recommendations
    print("\n🔍 NEXT STEPS FOR EDA:")
    print("1. 📊 Load cleaned datasets for exploratory analysis")
    print("2. 🔗 Identify common keys for dataset merging")
    print("3. 📈 Generate descriptive statistics")
    print("4. 📉 Create visualizations")
    print("5. 🔍 Identify patterns and relationships")
    
    return cleaned_files

# Main execution
if __name__ == "__main__":
    # Step 1: Inspect all datasets
    files_inventory = inspect_dataset_files()
    
    # Step 2: Clean each dataset
    print("\n🚀 Starting data cleaning process...")
    
    # Clean Box Office data
    bom_clean = clean_box_office_data()
    
    # Clean Movie Budgets data  
    budgets_clean = clean_movie_budgets_data()
    
    # Clean TMDb data
    tmdb_clean = clean_tmdb_data()
    
    # Clean Rotten Tomatoes movie info
    rt_info_clean = clean_rotten_tomatoes_info()
    
    # Clean Rotten Tomatoes reviews
    rt_reviews_clean = clean_rotten_tomatoes_reviews()
    
    # Extract and clean IMDb data
    imdb_tables = extract_and_clean_imdb_data()
    
    # Step 3: Generate summary report
    cleaned_files = generate_cleaning_summary()
    
    print("\n🎉 DATA CLEANING COMPLETE!")
    print("="*60)
    print("All datasets have been cleaned and saved to the Cleaned_Data folder.")
    print("You can now proceed with exploratory data analysis!")