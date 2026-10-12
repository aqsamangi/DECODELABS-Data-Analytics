
# DecodeLabs Data Analytics Projects

A collection of hands-on data analytics projects completed as part of the DecodeLabs Data Analytics training track. The projects cover data cleaning, exploratory data analysis, SQL querying, and data visualization.

## Projects

### Project 1: Data Cleaning and Preparation
**Goal:** Prepare the dataset for analysis by checking data quality.

- Identify and handle missing values.
- Check for duplicate records and IDs.
- Correct date, number, and text formats where necessary.
- Save the cleaned dataset for subsequent analysis.

### Project 2: Exploratory Data Analysis (EDA)
**Goal:** Understand the dataset's distributions, patterns, trends, and potential outliers.

- Calculate descriptive statistics, including mean, median, and count.
- Explore numerical and categorical variables.
- Identify patterns and unusual observations.
- Summarize findings based on the data.

### Project 3: SQL Data Analysis
**Goal:** Retrieve and summarize information using SQL.

- Retrieve records using `SELECT`.
- Filter data using `WHERE`.
- Sort results using `ORDER BY`.
- Group records using `GROUP BY`.
- Summarize data using aggregate functions such as `COUNT`, `SUM`, and `AVG`.

### Project 4: Data Visualization
**Goal:** Communicate data patterns and insights through suitable charts.

- Create appropriate visualizations for the dataset.
- Highlight important patterns and observations.
- Explain the insights communicated by each chart.

Note: Project 4 was described as an optional milestone in the training material.

## Dataset

The later projects use the cleaned dataset:

`Cleaned_Dataset_for_Data_Analytics.xlsx`

The cleaned dataset provides a consistent input for analysis and visualization.

## Tools and Technologies

- Python
- pandas
- NumPy, where needed
- Matplotlib and Seaborn, where used
- SQL
- Microsoft Excel
- Git and GitHub

## Repository Structure

The repository is organized into separate folders for each project.

```text
DecodeLabs-Data-Analytics/
├── Project-1-Data-Cleaning/
├── Project-2-EDA/
├── Project-3-SQL-Analysis/
├── Project-4-Data-Visualization/
└── README.md
```

Place each project's actual scripts, reports, query files, and generated charts in its corresponding folder.

## How to Run

The exact instructions depend on the files included in each project folder.

1. Download or clone this repository.
2. Open the folder for the project you want to run.
3. Install Python if the project uses Python scripts.
4. Install the libraries required by the script. For example:

   `pip install pandas openpyxl matplotlib seaborn`

5. Ensure the required input dataset is available at the file path specified in the script.
6. Open a terminal in the project folder and run:

   `python your_script_name.py`

   Replace `your_script_name.py` with the actual Python filename.

7. Check the terminal output and generated files to verify that the script ran successfully.

For Project 3, follow the SQL database setup and execution instructions included with the SQL files.

## Notes

- Use the cleaned dataset for the projects that require it.
- Base all findings and conclusions on actual analysis results.
- Keep project-specific instructions and output filenames updated.
- Only publish files you have permission to share. Check datasets and reports for confidential or sensitive information before making the repository public.
