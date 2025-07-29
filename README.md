# Movie Industry EDA Project

A comprehensive exploratory data analysis of movie industry data, including box office performance, ratings, budgets, and trends. This project provides cleaned datasets and thorough analysis notebooks ready for use in VS Code.

## 📋 Project Overview

This project analyzes **37,246 movie records** from multiple sources to uncover insights about:
- Movie performance trends and box office patterns
- Rating distributions across different platforms
- Budget vs revenue relationships and ROI analysis
- Genre popularity and performance over time
- Studio performance and market share analysis
- Temporal trends in the movie industry

## 🗂️ Project Structure

```
movie-eda-project/
│
├── README.md                              # This file
├── notebooks/                             # Jupyter notebooks
│   ├── 01_data_cleaning_complete.ipynb   # Data cleaning pipeline
│   └── 02_exploratory_data_analysis.ipynb # Comprehensive EDA
│
├── Original_Data/                         # Raw datasets (6 files)
│   ├── bom.movie_gross.csv.gz            # Box Office Mojo data
│   ├── tmdb.movies.csv.gz                # TMDb movie data
│   ├── tn.movie_budgets.csv.gz           # Movie budget data
│   ├── rt.movie_info.tsv.gz              # Rotten Tomatoes info
│   ├── rt.reviews.tsv                    # Rotten Tomatoes reviews
│   └── im.db.zip                         # IMDb database
│
├── cleaned_data/                          # Processed datasets
│   ├── tmdb_movies_cleaned.csv           # 26,517 records
│   ├── movie_budgets_cleaned.csv         # 5,782 records
│   ├── box_office_mojo_cleaned.csv       # 3,387 records
│   └── rotten_tomatoes_info_cleaned.csv  # 1,560 records
│
└── requirements.txt                       # Python dependencies
```

## 🚀 Getting Started with VS Code

### Step 1: Clone or Download the Project

**Option A: If you have the project locally**
```bash
# Navigate to your project directory
cd /path/to/your/movie-eda-project
```

**Option B: If transferring from another environment**
1. Copy all project files to your local machine
2. Maintain the directory structure shown above

### Step 2: Open in VS Code

1. **Open VS Code**
2. **Open the project folder:**
   - `File > Open Folder...`
   - Select your `movie-eda-project` directory
3. **Install the Python extension** (if not already installed):
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Python" by Microsoft
   - Click Install

### Step 3: Set Up Python Environment

1. **Create a virtual environment:**
   ```bash
   # In VS Code terminal (Terminal > New Terminal)
   python -m venv movie_eda_env
   
   # Activate the environment
   # On Windows:
   movie_eda_env\Scripts\activate
   # On macOS/Linux:
   source movie_eda_env/bin/activate
   ```

2. **Install required packages:**
   ```bash
   pip install pandas numpy matplotlib seaborn plotly jupyter ipykernel
   ```

3. **Select the Python interpreter:**
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose the interpreter from your virtual environment

### Step 4: Install Jupyter Extension

1. **Install Jupyter extension:**
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Jupyter"
   - Install "Jupyter" by Microsoft

2. **Verify setup:**
   - Open `notebooks/01_data_cleaning_complete.ipynb`
   - VS Code should recognize it as a Jupyter notebook
   - You should see "Select Kernel" option - choose your Python environment

## 📊 Working with the Notebooks

### Notebook 1: Data Cleaning (`01_data_cleaning_complete.ipynb`)

**Purpose:** Comprehensive data cleaning pipeline for all movie datasets

**Key Features:**
- Loads and cleans 4 major movie datasets
- Handles missing values and duplicates
- Standardizes data types and formats
- Cleans financial data (removes currency formatting)
- Exports clean datasets to `cleaned_data/` folder

**How to Use:**
1. Open the notebook in VS Code
2. Run cells sequentially (Shift+Enter)
3. Monitor data quality improvements
4. Review exported clean datasets

### Notebook 2: Exploratory Data Analysis (`02_exploratory_data_analysis.ipynb`)

**Purpose:** Comprehensive analysis of cleaned movie data

**Key Features:**
- Statistical analysis of movie performance
- Visualization of trends and patterns
- Rating distribution analysis
- Financial performance insights
- Genre and studio analysis
- Temporal trend analysis

**How to Use:**
1. Ensure you've run the data cleaning notebook first
2. Open the EDA notebook
3. Run cells to generate visualizations and insights
4. Modify analysis parameters as needed

## 🔧 Customizing the Analysis

### Adding New Analysis

1. **Create new cells** in the EDA notebook
2. **Use the cleaned datasets** from `cleaned_data/` folder
3. **Follow the existing pattern:**
   ```python
   # Analysis code with clear comments
   # ... your analysis here ...
   ```
   
   ```markdown
   ### Analysis Results
   
   **Key Findings:**
   - Finding 1 with explanation
   - Finding 2 with context
   - Insights and implications
   ```

### Working with Additional Data

1. **Add new data files** to `Original_Data/`
2. **Create cleaning code** in notebook 1
3. **Export cleaned data** to `cleaned_data/`
4. **Integrate analysis** in notebook 2

## 📤 Publishing to GitHub

### Step 1: Initialize Git Repository

```bash
# In your project directory
git init
git add .
git commit -m "Initial commit: Movie EDA project with cleaned datasets and analysis notebooks"
```

### Step 2: Create GitHub Repository

1. **Go to GitHub.com**
2. **Click "New repository"**
3. **Repository settings:**
   - Name: `movie-industry-eda`
   - Description: `Comprehensive exploratory data analysis of movie industry data`
   - Set to Public or Private as desired
   - **Do NOT** initialize with README (we already have one)
4. **Click "Create repository"**

### Step 3: Connect and Push

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/movie-industry-eda.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: GitHub Best Practices

1. **Create a .gitignore file:**
   ```bash
   # Create .gitignore
   echo "# Python
   __pycache__/
   *.pyc
   .env
   movie_eda_env/
   
   # Jupyter
   .ipynb_checkpoints/
   
   # VS Code
   .vscode/
   
   # Data files (optional - uncomment if datasets are very large)
   # Original_Data/
   # cleaned_data/" > .gitignore
   ```

2. **Regular commits:**
   ```bash
   # After making changes
   git add .
   git commit -m "Add financial analysis visualizations"
   git push
   ```

3. **Use branches for features:**
   ```bash
   # Create feature branch
   git checkout -b feature/genre-analysis
   
   # Work on your feature, then merge
   git checkout main
   git merge feature/genre-analysis
   ```

## 🔍 Dataset Descriptions

### TMDb Movies (26,517 records)
- **Source:** The Movie Database
- **Key Columns:** title, release_date, popularity, vote_average, vote_count, genre_ids
- **Use Cases:** Rating analysis, popularity trends, release patterns

### Movie Budgets (5,782 records)
- **Source:** The Numbers
- **Key Columns:** movie, release_date, production_budget, domestic_gross, worldwide_gross
- **Use Cases:** ROI analysis, budget vs revenue relationships, financial performance

### Box Office Mojo (3,387 records)
- **Source:** Box Office Mojo
- **Key Columns:** title, studio, domestic_gross, foreign_gross, year
- **Use Cases:** Studio performance, domestic vs international markets

### Rotten Tomatoes (1,560 records)
- **Source:** Rotten Tomatoes
- **Key Columns:** rating, genre, director, runtime, studio
- **Use Cases:** Critical analysis, genre performance, director success

## 🛠️ Troubleshooting

### Common Issues

1. **Kernel not found:**
   - Ensure Jupyter extension is installed
   - Select correct Python interpreter
   - Restart VS Code

2. **Import errors:**
   - Verify virtual environment is activated
   - Install missing packages with pip

3. **File not found errors:**
   - Check file paths are correct
   - Ensure you're in the project root directory

4. **Large file issues on GitHub:**
   - Use Git LFS for files > 100MB
   - Consider adding large data files to .gitignore

### Getting Help

- **VS Code Jupyter:** [Official Documentation](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
- **Pandas Documentation:** [pandas.pydata.org](https://pandas.pydata.org/)
- **Git/GitHub:** [GitHub Docs](https://docs.github.com/)

## 📈 Next Steps

1. **Run the analysis** notebooks to generate insights
2. **Customize visualizations** for your specific interests
3. **Add new research questions** and analysis
4. **Share findings** by pushing to GitHub
5. **Create presentations** or reports from your findings

---

**Happy Analyzing! 🎬📊**

*This project provides a solid foundation for movie industry analysis. Feel free to extend, modify, and share your insights!*

