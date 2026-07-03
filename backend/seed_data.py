"""Course seed data for CDAM Python for Data Science and Machine Learning.
Defines 18 comprehensive sessions:
- Sessions 1-10: Introduction to Python for Data Science (Beginner)
- Sessions 11-18: Master Python for Data Science and Machine Learning (Professional)
"""

SESSIONS = [
    {
        "title": "Session 1: Introduction to Python, Jupyter Notebook, and Basic Data Types",
        "slug": "session-1-intro-to-python-jupyter",
        "description": "Get started with Python syntax, Jupyter Notebook environment, and core variables.",
        "duration": "45 min",
        "difficulty": "Beginner",
        "objectives": """- Set up Python and launch Jupyter Notebook / JupyterLab
- Understand basic variables, data types, and arithmetic operators
- Execute print statements and basic interactive python cells""",
        "expected_outcomes": """- Launch a Jupyter Notebook local server.
- Declare variables of type int, float, string, and boolean.
- Write simple computational formulas using Python arithmetic.""",
        "learning_notes": """### Python & Jupyter Overview
Python is a general-purpose programming language popular for its readability. Jupyter Notebooks allow you to mix markdown explanations with executable python code blocks in a web browser.

### Primitive Types
- `int`: Integers (e.g. 5, -12)
- `float`: Decimals (e.g. 3.14, 0.0)
- `str`: Text wrapped in single or double quotes
- `bool`: True or False value""",
        "instructions": "Run the code editor cell to calculate variable values and print their types.",
        "content": "In this session, you will get comfortable executing commands in Python, declaring variables, and printing outcomes.",
        "code_examples": """# Declare variables and print types
name = "CDAM Student"
age = 20
gpa = 3.8
print(f"Student: {name}, Age: {age}, GPA: {gpa}")
print(type(name), type(age), type(gpa))""",
        "resources": "- [Python Official Tutorial](https://docs.python.org/3/tutorial/)\\n- [Jupyter Notebook Docs](https://jupyter-notebook.readthedocs.io/)",
        "quiz": [
            {"question": "Which of the following is a float in Python?", "options": ["3.14", "3", "'3.14'", "True"], "correct": 0},
            {"question": "How do you start a single-line comment in Python?", "options": ["#", "//", "/*", "<!--"], "correct": 0},
            {"question": "What is the result of type(True)?", "options": ["bool", "str", "int", "float"], "correct": 0}
        ]
    },
    {
        "title": "Session 2: Data Import, Cleaning, and Exploratory Data Analysis (EDA)",
        "slug": "session-2-data-import-eda",
        "description": "Learn how to read CSV files, locate missing values, and execute basic cleaning operations.",
        "duration": "50 min",
        "difficulty": "Beginner",
        "objectives": """- Read external files into memory
- Locate missing or Null values in a dataset
- Use pandas dropna and fillna techniques to clean up data""",
        "expected_outcomes": """- Load a dictionary or CSV file into a Pandas DataFrame.
- Clean missing entries using listwise deletion or imputation.
- Compute general statistics.""",
        "learning_notes": """### Exploratory Data Analysis (EDA)
EDA is the initial phase of data analysis where you inspect summary stats, detect outliers, and check completeness.

### Cleaning Techniques
- `dropna()`: Remove rows or columns containing missing values.
- `fillna()`: Replace missing values with static values or calculated column means.""",
        "instructions": "Execute the pandas code to see how rows containing Null or None values are deleted from the DataFrame.",
        "content": "Cleaning data is 80% of any data scientist's job. Learn to load and filter out bad rows.",
        "code_examples": """import pandas as pd
# Import and clean a sample dataset
data = {'Name': ['Alice', 'Bob', 'Carol', None], 'Age': [25, None, 30, 22]}
df = pd.DataFrame(data)
print("Original:")
print(df)
df_clean = df.dropna()
print("\\nCleaned:")
print(df_clean)""",
        "resources": "- [Pandas IO Docs](https://pandas.pydata.org/docs/user_guide/io.html)",
        "quiz": [
            {"question": "Which pandas function drops rows with missing values?", "options": ["dropna()", "fillna()", "drop()", "remove_nulls()"], "correct": 0},
            {"question": "What does EDA stand for?", "options": ["Exploratory Data Analysis", "Efficient Data Aggregation", "Estimated Domain Association", "Error Detection Assessment"], "correct": 0},
            {"question": "Which parameter in pandas is used to load custom missing value markers?", "options": ["na_values", "null_marker", "empty_vals", "fill_na"], "correct": 0}
        ]
    },
    {
        "title": "Session 3: Data Manipulation with pandas",
        "slug": "session-3-pandas-data-manipulation",
        "description": "Filter columns, select rows by condition, and group statistics with pandas.",
        "duration": "60 min",
        "difficulty": "Beginner",
        "objectives": """- Select columns and filter rows using logical indices
- Apply groupby operations to aggregate numeric metrics
- Pivot tables for multi-dimensional data analysis""",
        "expected_outcomes": """- Query datasets using conditional statements.
- Group rows by categorical values and sum their metrics.
- Produce custom slices of a DataFrame.""",
        "learning_notes": """### Data Manipulation
DataFrames represent tables. We filter using boolean expressions (e.g. `df[df['Score'] > 80]`). Grouping merges rows based on a target category and applies aggregate operations like `.sum()`, `.mean()`, or `.count()`.""",
        "instructions": "Run the code to filter the sample sales data and compute aggregated sum metrics.",
        "content": "Mastering DataFrame filtering and grouping allows you to answer quick business and academic questions.",
        "code_examples": """import pandas as pd
# Filter and aggregate data
sales = {'Region': ['East', 'West', 'East', 'West'], 'Revenue': [100, 150, 200, 300]}
df = pd.DataFrame(sales)
east_only = df[df['Region'] == 'East']
print("East Only:")
print(east_only)
print("\\nGrouped Revenue:")
print(df.groupby('Region').sum())""",
        "resources": "- [Pandas Indexing Tutorial](https://pandas.pydata.org/docs/user_guide/indexing.html)",
        "quiz": [
            {"question": "Which statement extracts column 'Revenue'?", "options": ["df['Revenue']", "df.get_row('Revenue')", "df.select('Revenue')", "df.loc_col('Revenue')"], "correct": 0},
            {"question": "How do you compute grouping metrics on categories in pandas?", "options": ["groupby()", "pivot()", "aggregate()", "join()"], "correct": 0},
            {"question": "How do you combine multiple filters in pandas?", "options": ["Using & and | operators", "Using and / or keywords", "Using join", "Nesting functions"], "correct": 0}
        ]
    },
    {
        "title": "Session 4: Data Visualization with matplotlib and seaborn",
        "slug": "session-4-matplotlib-seaborn-viz",
        "description": "Create charts, customize axes labels, and build visual heatmaps for presentations.",
        "duration": "60 min",
        "difficulty": "Beginner",
        "objectives": """- Generate line charts and bar plots using matplotlib
- Customize colors, titles, and legends
- Build scatter plots and correlation heatmaps with seaborn""",
        "expected_outcomes": """- Build charts with labeled axes.
- Select appropriate chart styles for categorical vs continuous data.
- Save visualizations as image files.""",
        "learning_notes": """### Data Visualization
Visualizations help communicate trends.
- `matplotlib.pyplot` is the core library for plotting.
- `seaborn` provides higher-level aesthetic defaults built on top of matplotlib.""",
        "instructions": "Generate and print confirmation of chart building using the code cell.",
        "content": "Charts are the language of data science. Let's learn to build and customize them.",
        "code_examples": """import matplotlib.pyplot as plt
# Plot simple line chart
x = [1, 2, 3, 4]
y = [10, 20, 25, 30]
plt.plot(x, y, marker='o', color='red')
plt.title("Sample Performance Chart")
plt.xlabel("Hours Studied")
plt.ylabel("Score")
print("Chart ready for rendering!")""",
        "resources": "- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)\\n- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)",
        "quiz": [
            {"question": "Which alias is commonly used for matplotlib.pyplot?", "options": ["plt", "mpl", "plot", "pyplot"], "correct": 0},
            {"question": "Which plot is ideal for showing continuous variables' correlations?", "options": ["Scatter plot", "Bar chart", "Pie chart", "Histogram"], "correct": 0},
            {"question": "How do you add a title to a matplotlib plot?", "options": ["plt.title('My Title')", "plt.set_title('My Title')", "plt.header('My Title')", "plt.label('My Title')"], "correct": 0}
        ]
    },
    {
        "title": "Session 5: Hypothesis Testing",
        "slug": "session-5-hypothesis-testing",
        "description": "Learn statistical inference: define null hypotheses and compute p-values.",
        "duration": "60 min",
        "difficulty": "Beginner",
        "objectives": """- Define null and alternative hypotheses
- Execute a one-sample and two-sample t-test
- Interpret p-values and make statistical decisions""",
        "expected_outcomes": """- Formulate statistical hypotheses.
- Run t-tests using scipy.stats.
- Determine statistical significance (e.g. at alpha=0.05).""",
        "learning_notes": """### Hypothesis Testing
Hypothesis tests verify if a sample observation differs significantly from a population mean or control group.
- **Null Hypothesis (H0)**: No effect or no difference.
- **P-value**: Probability of getting results at least as extreme, assuming H0 is true. If p < 0.05, we reject H0.""",
        "instructions": "Execute the t-test on student scores to calculate the t-statistic and the p-value.",
        "content": "Hypothesis testing helps prove whether your data trends are real or simply random noise.",
        "code_examples": """import scipy.stats as stats
# Perform a one-sample t-test
scores = [78, 85, 92, 88, 79, 81, 95, 87]
t_stat, p_val = stats.ttest_1samp(scores, popmean=80)
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_val:.4f}")""",
        "resources": "- [SciPy Stats Tutorial](https://docs.scipy.org/doc/scipy/tutorial/stats.html)",
        "quiz": [
            {"question": "If p-value is 0.02 and alpha is 0.05, what do you do?", "options": ["Reject the null hypothesis", "Fail to reject the null hypothesis", "Increase alpha value", "Discard the dataset"], "correct": 0},
            {"question": "What test compares the means of two independent groups?", "options": ["Two-sample independent t-test", "One-sample t-test", "Chi-square test", "ANOVA"], "correct": 0},
            {"question": "What does a t-test measure?", "options": ["Difference between group means relative to variance", "Standard deviation of one group", "Correlation coefficient", "Outlier count"], "correct": 0}
        ]
    },
    {
        "title": "Session 6: Correlation and Regression Analysis",
        "slug": "session-6-correlation-regression",
        "description": "Measure associations between variables and build linear models.",
        "duration": "75 min",
        "difficulty": "Beginner",
        "objectives": """- Calculate Pearson correlation coefficients
- Build and evaluate a linear regression line
- Interpret regression slopes, intercepts, and R-squared values""",
        "expected_outcomes": """- Calculate correlation using scipy.stats.
- Fit a linear regression line.
- Predict output values for new inputs using the regression equation.""",
        "learning_notes": """### Correlation vs Causation
Correlation measures strength and direction of linear association. Pearson's r values range from -1 to 1.
Linear regression computes:
`y = slope * x + intercept`
It represents the line of best fit through the data points.""",
        "instructions": "Run the code to calculate both correlation and linear regression parameters.",
        "content": "Regression analysis is the foundation of predictive analytics. Learn to trace trends and forecast variables.",
        "code_examples": """import numpy as np
import scipy.stats as stats
# Correlation between study hours and exam scores
hours = [2, 4, 6, 8, 10]
scores = [55, 65, 75, 80, 95]
corr, p = stats.pearsonr(hours, scores)
slope, intercept, r, p_val, std_err = stats.linregress(hours, scores)
print(f"Correlation Coefficient: {corr:.4f}")
print(f"Regression Line: y = {slope:.2f}x + {intercept:.2f}")""",
        "resources": "- [SciPy linregress Docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html)",
        "quiz": [
            {"question": "What does a correlation coefficient of -0.9 indicate?", "options": ["Strong negative correlation", "Strong positive correlation", "Weak negative correlation", "No correlation"], "correct": 0},
            {"question": "In y = mx + c, what does m represent?", "options": ["Slope", "Y-intercept", "Residual value", "Mean of x"], "correct": 0},
            {"question": "What is the range of Pearson's correlation coefficient?", "options": ["-1 to 1", "0 to 1", "-inf to inf", "0 to 100"], "correct": 0}
        ]
    },
    {
        "title": "Session 7: Analysis of Variance (ANOVA) and Non-Parametric Tests",
        "slug": "session-7-anova-tests",
        "description": "Compare multiple means with ANOVA and check categorical counts with Chi-square.",
        "duration": "75 min",
        "difficulty": "Beginner",
        "objectives": """- Run a One-Way ANOVA test across three or more cohorts
- Understand assumptions of ANOVA (normality, variance homogeneity)
- Perform non-parametric alternatives when normality is violated""",
        "expected_outcomes": """- Execute an ANOVA F-test.
- Use Chi-Square or Kruskal-Wallis tests.
- Evaluate treatment effects across multiple groups.""",
        "learning_notes": """### ANOVA (Analysis of Variance)
ANOVA compares the means of three or more independent groups to see if at least one group mean is statistically different.
If normality assumptions are violated, use non-parametric tests like Kruskal-Wallis.""",
        "instructions": "Run the code to perform a One-Way ANOVA test on three sample education methods.",
        "content": "Compare multiple groups at once and verify if variation comes from real treatment differences or random sampling.",
        "code_examples": """import scipy.stats as stats
# One-way ANOVA test for three study methods
method_A = [85, 88, 90, 82]
method_B = [72, 75, 80, 78]
method_C = [91, 95, 88, 92]
f_stat, p_val = stats.f_oneway(method_A, method_B, method_C)
print(f"F-statistic: {f_stat:.4f}")
print(f"P-value: {p_val:.4f}")""",
        "resources": "- [ANOVA on Wikipedia](https://en.wikipedia.org/wiki/Analysis_of_variance)",
        "quiz": [
            {"question": "What null hypothesis does One-Way ANOVA test?", "options": ["All group means are equal", "At least one group mean is different", "Group variances are unequal", "The data is normally distributed"], "correct": 0},
            {"question": "Which test is a non-parametric alternative to ANOVA?", "options": ["Kruskal-Wallis test", "Independent t-test", "Chi-square test", "Paired t-test"], "correct": 0},
            {"question": "What is verified by checking ANOVA assumptions?", "options": ["Normality and Homoscedasticity", "Linearity and independence only", "Multicollinearity", "Accuracy score"], "correct": 0}
        ]
    },
    {
        "title": "Session 8: Time Series Analysis",
        "slug": "session-8-time-series",
        "description": "Understand date indexes, resample time logs, and compute rolling moving averages.",
        "duration": "75 min",
        "difficulty": "Beginner",
        "objectives": """- Convert strings to Datetime indexes
- Compute rolling window averages to smooth trends
- Resample time series to hourly, daily, or monthly frequencies""",
        "expected_outcomes": """- Create a DatetimeIndex in a Pandas DataFrame.
- Apply rolling window operations.
- Extract trend and seasonal directions from logs.""",
        "learning_notes": """### Time Series Data
A time series is a sequence of observations taken sequentially in time.
- `resample()`: Aggregates time frequencies (e.g. sum daily logs into weekly totals).
- `rolling()`: Calculates statistics in a moving window, smoothing out noise.""",
        "instructions": "Execute the code to create a date-indexed series and calculate a moving average.",
        "content": "Time series analysis is essential for financial markets, weather tracking, and demand forecasting.",
        "code_examples": """import pandas as pd
# Time series index and rolling mean
dates = pd.date_range(start="2024-01-01", periods=5, freq="D")
values = [100, 105, 98, 110, 115]
ts = pd.Series(values, index=dates)
print("Time Series:")
print(ts)
print("\\n2-Day Rolling Mean:")
print(ts.rolling(window=2).mean())""",
        "resources": "- [Pandas Time Series Guide](https://pandas.pydata.org/docs/user_guide/timeseries.html)",
        "quiz": [
            {"question": "How do you parse string date formats in pandas?", "options": ["pd.to_datetime()", "pd.as_time()", "df.format_dates()", "df.parse_time()"], "correct": 0},
            {"question": "What does df.rolling(window=7).mean() compute?", "options": ["7-period moving average", "Mean of every 7th row", "Total sum of 7 columns", "Cumulative sum"], "correct": 0},
            {"question": "Which pandas function rescales time frequencies?", "options": ["resample()", "groupby()", "reindex()", "shift()"], "correct": 0}
        ]
    },
    {
        "title": "Session 9: Reporting with Jupyter Notebook",
        "slug": "session-9-jupyter-reporting",
        "description": "Generate clean reports, insert markdown explanations, and configure notebook layouts.",
        "duration": "60 min",
        "difficulty": "Beginner",
        "objectives": """- Format headers, bold text, and equations in markdown cells
- Hide raw code blocks for client presentations
- Export notebooks to HTML or PDF formats""",
        "expected_outcomes": """- Structure notebooks with clear sections.
- Create professional executive report summaries.
- Configure clean notebook presentation layouts.""",
        "learning_notes": """### Notebook Reports
Jupyter Notebook is not just a coding console — it is a document tool.
Use markdown headings (`#`, `##`, `###`) to structure sections and write key findings to support numerical analytics results.""",
        "instructions": "Run the cell to generate a simulated executive academic report summary.",
        "content": "Learn how to structure your findings into an executive report format that decision makers can understand.",
        "code_examples": """# Simulate generating a report summary
student_count = 150
passing_pct = 94.2
report = f'''
--- CDAM ACADEMIC REPORT ---
Total Students Evaluated: {student_count}
Curriculum Completion Rate: {passing_pct}%
Recommendation: Advance to Machine Learning module.
'''
print(report)""",
        "resources": "- [Jupyter Markdown Guide](https://www.markdownguide.org/tools/jupyter-notebook/)",
        "quiz": [
            {"question": "Which markdown tag creates a main header in a Jupyter cell?", "options": ["# Header", "## Header", "**Header**", "<h1>Header"], "correct": 0},
            {"question": "What tool exports Jupyter Notebooks to HTML/PDF?", "options": ["nbconvert", "pdfmaker", "jupconvert", "exporter"], "correct": 0},
            {"question": "How can you run all cells in Jupyter at once?", "options": ["Cell -> Run All", "Ctrl + Enter", "Alt + Shift", "Run File"], "correct": 0}
        ]
    },
    {
        "title": "Session 10: Capstone Project",
        "slug": "session-10-capstone-beginner",
        "description": "Demonstrate your data skills: import, clean, analyze, and present a sample dataset.",
        "duration": "90 min",
        "difficulty": "Beginner",
        "objectives": """- Integrate EDA, cleaning, and aggregation into a single script
- Calculate summary stats and draw statistical conclusions
- Output a clean report summary showing student insights""",
        "expected_outcomes": """- Implement a full data pipeline from scratch.
- Clean and analyze multi-class performance parameters.
- Provide statistical outcomes.""",
        "learning_notes": """### Capstone Integration
The capstone combines everything you have learned in the Beginner course: basic variables, cleaning, grouping, statistical analysis, and markdown presentation of results.""",
        "instructions": "Execute the capstone simulation code to analyze multi-level student performances.",
        "content": "Verify your beginner mastery by completing this end-to-end data analytics workflow.",
        "code_examples": """import pandas as pd
# Beginner Capstone Simulation
# Perform full flow: Import -> Clean -> Group -> Output Statistics
raw_data = {'ID': [1, 2, 3, 4], 'Level': ['Beginner', 'Beginner', 'Advanced', 'Advanced'], 'Score': [85, 78, 92, 88]}
df = pd.DataFrame(raw_data)
summary = df.groupby('Level')['Score'].mean()
print("CDAM Capstone Executive Summary:")
print(summary)""",
        "resources": "- [CDAM Graduation Portal](https://cdam.chuka.ac.ke/grad/)",
        "quiz": [
            {"question": "What is the first step of a standard data pipeline?", "options": ["Data ingestion / import", "Statistical modeling", "Data visualization", "Model deployment"], "correct": 0},
            {"question": "What does groupby aggregate functions return?", "options": ["Summary metrics matching categories", "Raw lists of strings", "The original un-aggregated rows", "JSON templates"], "correct": 0},
            {"question": "Why is keeping a code log important?", "options": ["For reproducibility of results", "To speed up server responses", "To save memory space", "It is not important"], "correct": 0}
        ]
    },
    {
        "title": "Session 11: Advanced Data Wrangling with pandas",
        "slug": "session-11-advanced-pandas",
        "description": "Learn multi-index, merge operations, and pivot tables to reshape complex tables.",
        "duration": "60 min",
        "difficulty": "Professional",
        "objectives": """- Merge, join, and concatenate multiple DataFrames
- Construct pivot tables with custom aggregation columns
- Reshape tables using stack, unstack, and melt operations""",
        "expected_outcomes": """- Build multi-level index tables.
- Combine datasets using relational keys.
- Pivot long-format datasets into wide-format datasets.""",
        "learning_notes": """### Relational Operations & Pivoting
In professional environments, data is split. Use `pd.merge()` to perform database-style inner, outer, left, and right joins.
`pivot_table()` builds summary tables similar to Excel pivot tools, grouping metrics by multiple indexes.""",
        "instructions": "Execute the pivot table simulation to see expense metrics grouped by year and department.",
        "content": "Reshape, combine, and organize high-dimensional tables to extract insights.",
        "code_examples": """import pandas as pd
# Advanced pivot tables and multi-indexing
data = {'Year': [2023, 2023, 2024, 2024], 'Dept': ['HR', 'IT', 'HR', 'IT'], 'Expense': [50000, 75000, 52000, 80000]}
df = pd.DataFrame(data)
pivot = df.pivot_table(values='Expense', index='Year', columns='Dept', aggfunc='sum')
print(pivot)""",
        "resources": "- [Pandas Reshaping Documentation](https://pandas.pydata.org/docs/user_guide/reshaping.html)",
        "quiz": [
            {"question": "Which pandas function performs database-style joins?", "options": ["pd.merge()", "pd.concat()", "pd.join_only()", "pd.pivot()"], "correct": 0},
            {"question": "What is the opposite of pivoting wide data (melting)?", "options": ["Melting wide to long", "Reshaping index", "Joining categories", "Grouping"], "correct": 0},
            {"question": "How do you stack a DataFrame column index?", "options": ["df.stack()", "df.unstack()", "df.pivot()", "df.groupby()"], "correct": 0}
        ]
    },
    {
        "title": "Session 12: Functional Programming & Efficient Coding",
        "slug": "session-12-functional-programming",
        "description": "Optimize your loops with lambda, map, filter, and list comprehensions.",
        "duration": "60 min",
        "difficulty": "Professional",
        "objectives": """- Write lambda (anonymous) functions for fast computations
- Use map() and filter() generators to process sequences
- Construct list and dictionary comprehensions for clean code""",
        "expected_outcomes": """- Eliminate slow, nested for loops.
- Apply lambda formulas across DataFrame rows.
- Build clean list comprehensions.""",
        "learning_notes": """### Functional Programming
Functional styles avoid mutating state.
- `lambda`: Simple inline functions.
- `map(func, iterable)`: Applies a function to all elements.
- `filter(pred, iterable)`: Keeps elements matching a condition.""",
        "instructions": "Run the code to compare functional map/filter against clean list comprehensions.",
        "content": "Functional methods make your python pipelines run faster and look cleaner.",
        "code_examples": """# Lambda, map, filter, list comprehensions
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squared_evens = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
print("Squared Evens:", squared_evens)
# Comprehension alternative
comp = [x**2 for x in numbers if x % 2 == 0]
print("Comprehension matches:", comp == squared_evens)""",
        "resources": "- [Python Functional Programming HowTo](https://docs.python.org/3/howto/functional.html)",
        "quiz": [
            {"question": "What keyword defines anonymous inline functions?", "options": ["lambda", "anonymous", "def", "inline"], "correct": 0},
            {"question": "Which structure replaces map and filter cleanly?", "options": ["List comprehension", "While loop", "Try-Except block", "Class definition"], "correct": 0},
            {"question": "Is list comprehension generally faster than manual for loops?", "options": ["Yes, it is optimized in C", "No, it is identical", "No, it is slower", "Only on Windows"], "correct": 0}
        ]
    },
    {
        "title": "Session 13: Advanced Data Visualization (matplotlib & seaborn)",
        "slug": "session-13-advanced-visualization",
        "description": "Build multi-panel grids, style correlation matrices, and customize plot settings.",
        "duration": "75 min",
        "difficulty": "Professional",
        "objectives": """- Build multi-panel subplots using fig, axes layouts
- Customize heatmap color maps and labels
- Configure publication-quality chart settings""",
        "expected_outcomes": """- Build multi-panel subplots grids.
- Generate annotated correlation matrix heatmaps.
- Save high-resolution charts suitable for academic papers.""",
        "learning_notes": """### Advanced Visualization
For complex analysis, one plot is not enough.
Use `plt.subplots(rows, cols)` to arrange multiple panels.
`seaborn.heatmap()` visualizes correlation tables, making numeric associations clear at a glance.""",
        "instructions": "Run the code to calculate a correlation matrix and simulate a heatmap output.",
        "content": "Learn how to build high-density visualizations that fit into scientific reports and business slides.",
        "code_examples": """import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# Correlation heatmap plotting simulation
data = {'StudyHours': [2, 5, 7, 8], 'PracticeScore': [60, 70, 85, 90], 'FinalExam': [55, 72, 88, 92]}
df = pd.DataFrame(data)
corr = df.corr()
print("Correlation Matrix:")
print(corr)
print("\\nHeatmap generated successfully.")""",
        "resources": "- [Seaborn Heatmap Docs](https://seaborn.pydata.org/generated/seaborn.heatmap.html)",
        "quiz": [
            {"question": "How do you create a 2x2 subplot grid in matplotlib?", "options": ["plt.subplots(2, 2)", "plt.grid(2, 2)", "plt.panels(2, 2)", "plt.axes_grid(2, 2)"], "correct": 0},
            {"question": "Which seaborn function plots correlation grids?", "options": ["heatmap()", "barplot()", "boxplot()", "scatterplot()"], "correct": 0},
            {"question": "How do you save a matplotlib chart to a high-res image file?", "options": ["plt.savefig('name.png', dpi=300)", "plt.write('name.png')", "plt.export('name.png')", "plt.save('name.png')"], "correct": 0}
        ]
    },
    {
        "title": "Session 14: Statistical Modeling & Hypothesis Testing",
        "slug": "session-14-statistical-modeling",
        "description": "Construct Ordinary Least Squares (OLS) regression models and evaluate p-values.",
        "duration": "75 min",
        "difficulty": "Professional",
        "objectives": """- Build multivariate linear regression models using statsmodels
- Interpret model summary tables: R-squared, coefficients, and F-statistic
- Diagnose regression assumptions (residuals normality, collinearity)""",
        "expected_outcomes": """- Build linear models using statsmodels API.
- Evaluate model goodness-of-fit.
- Interpret coefficient confidence intervals.""",
        "learning_notes": """### Ordinary Least Squares (OLS)
OLS regression models the relationship between dependent and independent variables.
- **R-squared**: Percentage of variance in the target explained by the predictors.
- **P>|t|**: P-value checking if predictor coefficients are significantly different from 0.""",
        "instructions": "Execute the OLS linear model to output the statistical summary table.",
        "content": "Build linear models that explain the factors driving your target variables.",
        "code_examples": """import statsmodels.api as sm
import pandas as pd
# Ordinary Least Squares (OLS) Regression
data = {'StudyHours': [2, 4, 6, 8, 10], 'ExamScore': [50, 60, 70, 80, 95]}
df = pd.DataFrame(data)
X = sm.add_constant(df['StudyHours'])
model = sm.OLS(df['ExamScore'], X).fit()
print(model.summary().tables[1])""",
        "resources": "- [Statsmodels OLS Guide](https://www.statsmodels.org/stable/regression.html)",
        "quiz": [
            {"question": "What does a high R-squared indicate?", "options": ["Model explains a large portion of variance", "Model is statistically insignificant", "Residuals are not normal", "Perfect accuracy"], "correct": 0},
            {"question": "Why do we add a constant column in statsmodels regression?", "options": ["To calculate the y-intercept", "To normalize the data", "To avoid division by zero", "It is optional"], "correct": 0},
            {"question": "Which metric evaluates overall model significance?", "options": ["F-statistic p-value", "R-squared value", "Intercept coefficient", "Standard error"], "correct": 0}
        ]
    },
    {
        "title": "Session 15: Machine Learning in Python (Supervised Learning)",
        "slug": "session-15-supervised-learning",
        "description": "Train linear classifiers, predict classes, and measure model accuracy.",
        "duration": "75 min",
        "difficulty": "Professional",
        "objectives": """- Understand differences between regression and classification
- Train a Logistic Regression model using scikit-learn
- Evaluate metrics: accuracy, precision, recall, and F1-score""",
        "expected_outcomes": """- Split datasets into training and testing sets.
- Train supervised models.
- Predict target classes for new inputs.""",
        "learning_notes": """### Supervised Learning
Supervised models learn from labeled pairs.
- **Classification**: Target is categorical (e.g. Pass/Fail, Spam/Ham).
- **Logistic Regression**: Outputs a probability score between 0 and 1, mapped to class labels.""",
        "instructions": "Execute the logistic classifier code to fit and predict test outcomes.",
        "content": "Train classification models that automatically label incoming data.",
        "code_examples": """from sklearn.linear_model import LogisticRegression
import numpy as np
# Logistic Regression classification simulation
X = np.array([[2.0], [1.0], [5.0], [8.0], [9.0]])
y = np.array([0, 0, 0, 1, 1])
model = LogisticRegression().fit(X, y)
print("Coefficients:", model.coef_)
print("Predict on study hours [6]:", model.predict([[6.0]]))""",
        "resources": "- [Scikit-Learn Supervised Learning Guide](https://scikit-learn.org/stable/supervised_learning.html)",
        "quiz": [
            {"question": "Which of these is a classification task?", "options": ["Predicting if an email is spam", "Predicting next month's sales", "Clustering users by behavior", "Sorting records"], "correct": 0},
            {"question": "What is the target parameter in supervised learning?", "options": ["Labeled training answers", "Unlabeled categories", "Number of columns", "File paths"], "correct": 0},
            {"question": "Which scikit-learn class trains logistic models?", "options": ["LogisticRegression", "LinearRegression", "KMeans", "DecisionTreeRegressor"], "correct": 0}
        ]
    },
    {
        "title": "Session 16: Unsupervised Learning & Dimensionality Reduction",
        "slug": "session-16-unsupervised-learning",
        "description": "Cluster data with K-Means and simplify columns with Principal Component Analysis.",
        "duration": "75 min",
        "difficulty": "Professional",
        "objectives": """- Differentiate supervised vs unsupervised learning paradigms
- Implement K-Means clustering to find patterns in unlabeled data
- Reduce features using PCA (Principal Component Analysis)""",
        "expected_outcomes": """- Build cluster segments.
- Reduce column dimensions with PCA.
- Interpret elbow plots to find optimal cluster sizes.""",
        "learning_notes": """### Unsupervised Clustering
Unsupervised algorithms find hidden structures in data without pre-existing labels.
- **K-Means**: Clusters data into K groups based on distances to cluster centers.
- **PCA**: Projects high-dimensional datasets onto principal axes to reduce dimensions while saving variance.""",
        "instructions": "Execute the clustering code to find cluster coordinates and labels.",
        "content": "Discover customer segments or group biological samples using clustering methods.",
        "code_examples": """from sklearn.cluster import KMeans
import numpy as np
# K-Means clustering simulation
X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])
kmeans = KMeans(n_clusters=2, random_state=0, n_init='auto').fit(X)
print("Cluster centers:")
print(kmeans.cluster_centers_)
print("Labels:", kmeans.labels_)""",
        "resources": "- [Scikit-Learn Clustering Docs](https://scikit-learn.org/stable/modules/clustering.html)",
        "quiz": [
            {"question": "What is unsupervised learning?", "options": ["Training models on unlabeled data", "Training models with supervised labels", "Running Python without a compiler", "None of the above"], "correct": 0},
            {"question": "Which parameter determines group counts in K-Means?", "options": ["n_clusters", "max_iter", "n_init", "random_state"], "correct": 0},
            {"question": "What does PCA stand for?", "options": ["Principal Component Analysis", "Predictive Categorical Association", "Pearson Correlation Analysis", "Polynomial Component Alignment"], "correct": 0}
        ]
    },
    {
        "title": "Session 17: Working with External Data Sources",
        "slug": "session-17-external-data-sources",
        "description": "Fetch remote JSON data from REST APIs and parse database schemas.",
        "duration": "60 min",
        "difficulty": "Professional",
        "objectives": """- Send API requests using Python requests library
- Parse hierarchical JSON responses into clean dicts
- Load fetched tables directly into Pandas DataFrames""",
        "expected_outcomes": """- Extract online JSON documents.
- Load unstructured API feeds into clean Pandas tables.
- Access public REST APIs.""",
        "learning_notes": """### REST APIs & JSON
Much of the world's data is stored in remote servers.
Web APIs return structured text formatted as JSON (JavaScript Object Notation). Use the requests library to send HTTP GET calls and unpack dictionary responses.""",
        "instructions": "Run the code to simulate parsing a JSON API server payload response.",
        "content": "Connect your analysis directly to live web databases and cloud data streams.",
        "code_examples": """import json
# Parsing and loading JSON response from APIs
json_response = '{"status": "success", "data": {"users": [{"name": "AI Coach", "role": "Tutor"}]}}'
parsed = json.loads(json_response)
print("API Response Status:", parsed['status'])
print("Coach Name:", parsed['data']['users'][0]['name'])""",
        "resources": "- [Python Requests Documentation](https://requests.readthedocs.io/)",
        "quiz": [
            {"question": "Which python library is standard for HTTP requests?", "options": ["requests", "json", "urllib_only", "socket"], "correct": 0},
            {"question": "What data format resembles Python dictionaries?", "options": ["JSON", "CSV", "XML", "YAML"], "correct": 0},
            {"question": "Which method parses a JSON string into a Python dict?", "options": ["json.loads()", "json.dumps()", "json.parse()", "json.dict()"], "correct": 0}
        ]
    },
    {
        "title": "Session 18: Reporting & Reproducibility",
        "slug": "session-18-reporting-reproducibility",
        "description": "Lock package versions, write requirements files, and package reproducible data reports.",
        "duration": "60 min",
        "difficulty": "Professional",
        "objectives": """- Build lockfiles and requirements.txt manifests
- Structure notebooks with seeds to guarantee statistical reproducibility
- Configure clean virtual environments for cloud deployments""",
        "expected_outcomes": """- Document pipeline environments.
- Enforce random seed states across models.
- Set up isolated pip virtual environments.""",
        "learning_notes": """### Scientific Reproducibility
A study is reproducible if another researcher can run the identical code on the same data and get the exact same results.
Always lock package versions (e.g. `pandas==2.1.1`) and enforce seeds in random algorithms.""",
        "instructions": "Run the script cell to generate a sample reproducible dependency manifest.",
        "content": "Verify your project will build identical results on any computer in the world.",
        "code_examples": """# Generate reproducible environment manifest summary
dependencies = {"python": "3.10.12", "pandas": "2.1.1", "numpy": "1.26.0", "scikit-learn": "1.3.0"}
print("CDAM Reproducible Environment Manifest:")
for pkg, ver in dependencies.items():
    print(f" - {pkg}=={ver}")
    print("Lockfile generated successfully.")""",
        "resources": "- [Pip Virtual Environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)",
        "quiz": [
            {"question": "Which file specifies project packages and versions?", "options": ["requirements.txt", "packages.json", "environment.html", "setup.py only"], "correct": 0},
            {"question": "Why do we set random seeds in machine learning models?", "options": ["To ensure identical results on every run", "To speed up model training times", "To optimize model performance", "To clean raw string inputs"], "correct": 0},
            {"question": "How do you install requirements in a new environment?", "options": ["pip install -r requirements.txt", "pip install requirements", "python run requirements", "git pull requirements"], "correct": 0}
        ]
    }
]

R_SESSIONS = [
    {
        "title": "Session 1: Introduction to R, RStudio, and Basic Data Types",
        "slug": "r-session-1-intro-to-r",
        "description": "Get started with R syntax, RStudio workspace, and basic variables.",
        "duration": "45 min",
        "difficulty": "Beginner",
        "objectives": """- Set up R and understand the RStudio workspace layout
- Understand variables, vectors, and basic numeric, character, and logical data types
- Execute print statements and run simple calculations in R console""",
        "expected_outcomes": """- Declare variables in R using the assignment operator (<-).
- Identify vector classes (numeric, character, logical).
- Run basic math operations on vectors.""",
        "learning_notes": """### R & RStudio Overview
R is a programming language specifically built for statistical computing and graphics. RStudio is the standard IDE for R.

### Assignment Operator
In R, we typically use `<-` instead of `=` for assignment:
`x <- 10`

### Core Data Types
- `numeric`: Decimals or integers (e.g., 3.14, 42)
- `character`: Text strings wrapped in quotes
- `logical`: TRUE or FALSE values (can be abbreviated as T or F)""",
        "instructions": "Run the code editor cell to calculate variable values and print their class.",
        "content": "Get comfortable writing basic R syntax, assigning variables, and checking their types.",
        "code_examples": """# Declare variables in R
name <- "CDAM Student"
age <- 20
gpa <- 3.8
print(paste("Student:", name, "Age:", age, "GPA:", gpa))
print(class(name))
print(class(age))""",
        "resources": "- [R Manuals](https://cran.r-project.org/manuals.html)\\n- [RStudio Desktop](https://posit.co/download/rstudio-desktop/)",
        "quiz": [
            {"question": "What is the standard assignment operator in R?", "options": ["<-", "=", "==", "assign"], "correct": 0},
            {"question": "How do you start a single-line comment in R?", "options": ["#", "//", "/*", "<!--"], "correct": 0},
            {"question": "Which function is used to check the data type of an object in R?", "options": ["class()", "type()", "typeof()", "datatype()"], "correct": 0}
        ]
    },
    {
        "title": "Session 2: Data Import, Cleaning, and Exploratory Data Analysis (EDA) in R",
        "slug": "r-session-2-data-import-eda",
        "description": "Learn to load CSV data, find missing variables, and perform basic data cleaning.",
        "duration": "50 min",
        "difficulty": "Beginner",
        "objectives": """- Read CSV files using base R read.csv
- Identify missing values (NA) in data frames
- Clean missing values using na.omit and basic imputation""",
        "expected_outcomes": """- Load a CSV file into an R data.frame.
- Detect missing entries with is.na().
- Filter out rows containing missing values.""",
        "learning_notes": """### Exploratory Data Analysis in R
We begin by inspecting data structures using `str()` and calculating summary stats using `summary()`.

### Missing Data (NA)
In R, missing values are represented by `NA`. We use `is.na(x)` to find them, and `na.omit()` to drop rows containing any NAs.""",
        "instructions": "Execute the R code to see how rows containing NA values are filtered from a data frame.",
        "content": "Clean datasets using R's built-in functions before starting analysis.",
        "code_examples": """# Create a sample data frame with NA values
df <- data.frame(
  Name = c("Alice", "Bob", "Carol", NA),
  Age = c(25, NA, 30, 22)
)
print("Original Data Frame:")
print(df)
df_clean <- na.omit(df)
print("Cleaned Data Frame:")
print(df_clean)""",
        "resources": "- [R Data Import/Export Guide](https://cran.r-project.org/doc/manuals/r-release/R-data.html)",
        "quiz": [
            {"question": "What value represents missing data in R?", "options": ["NA", "Null", "None", "NaN"], "correct": 0},
            {"question": "Which function drops rows with missing values in R?", "options": ["na.omit()", "is.na()", "drop_na()", "remove.na()"], "correct": 0},
            {"question": "Which function gives a quick summary statistics of a data frame?", "options": ["summary()", "str()", "head()", "describe()"], "correct": 0}
        ]
    },
    {
        "title": "Session 3: Data Manipulation with dplyr",
        "slug": "r-session-3-dplyr-manipulation",
        "description": "Filter rows, select columns, and calculate grouping summaries using dplyr.",
        "duration": "60 min",
        "difficulty": "Beginner",
        "objectives": """- Understand tidyverse and the pipe operator (%>% or |>)
- Use dplyr verbs: filter, select, mutate, and arrange
- Perform group summaries using group_by and summarize""",
        "expected_outcomes": """- Slice and subset data frames using dplyr verbs.
- Compute average scores for categories.
- Chain multiple operations using pipe syntax.""",
        "learning_notes": """### dplyr Manipulation
The `dplyr` package is the core tool of the Tidyverse for data manipulation:
- `filter()`: Keep rows matching criteria.
- `select()`: Pick columns by name.
- `mutate()`: Create or transform columns.
- `summarize()`: Aggregate values.

### Pipe Operator
The pipe operator `%>%` passes the result of one function as the first argument of the next.""",
        "instructions": "Run the dplyr script to filter sales data and aggregate revenue statistics.",
        "content": "Master dplyr to write readable, elegant data pipelines in R.",
        "code_examples": """library(dplyr)
# Create sales data
df <- data.frame(
  Region = c("East", "West", "East", "West"),
  Revenue = c(100, 150, 200, 300)
)
# Filter and summarize
east_only <- df %>% filter(Region == "East")
print("East Region only:")
print(east_only)
grouped <- df %>% group_by(Region) %>% summarize(Total = sum(Revenue))
print("Grouped Revenue:")
print(grouped)""",
        "resources": "- [dplyr Cheatsheet](https://github.com/rstudio/cheatsheets/blob/main/data-transformation.pdf)",
        "quiz": [
            {"question": "Which dplyr verb is used to subset rows?", "options": ["filter()", "select()", "mutate()", "slice()"], "correct": 0},
            {"question": "Which operator is the classical Tidyverse pipe?", "options": ["%>%", "%>%", "|>", "->"], "correct": 0},
            {"question": "How do you add new columns in dplyr?", "options": ["mutate()", "add()", "select()", "transform()"], "correct": 0}
        ]
    },
    {
        "title": "Session 4: Data Visualization with ggplot2",
        "slug": "r-session-4-ggplot2-visualization",
        "description": "Create publication-quality charts using the Grammar of Graphics.",
        "duration": "60 min",
        "difficulty": "Beginner",
        "objectives": """- Understand the layers of the Grammar of Graphics
- Create scatter plots, bar charts, and line plots with ggplot
- Customize themes, colors, and axis labels""",
        "expected_outcomes": """- Build charts using ggplot() and geom functions.
- Customize colors and labels.
- Save charts using ggsave().""",
        "learning_notes": """### ggplot2 & Grammar of Graphics
ggplot2 is built on the Grammar of Graphics, combining data, aesthetic mappings (`aes`), and geometric layers (`geom_`):
- `geom_point()`: Scatter plots.
- `geom_line()`: Line charts.
- `geom_bar()`: Bar charts.""",
        "instructions": "Execute the ggplot code to set up a sample line chart.",
        "content": "Create rich, multi-layered visual charts using ggplot2.",
        "code_examples": """library(ggplot2)
# Prepare data
df <- data.frame(
  Hours = c(1, 2, 3, 4),
  Score = c(10, 20, 25, 30)
)
# Construct line chart
p <- ggplot(df, aes(x=Hours, y=Score)) +
  geom_line(color="red") +
  geom_point(color="blue", size=3) +
  theme_minimal() +
  labs(title="Performance Chart", x="Hours", y="Score")
print("Plot structured successfully!")""",
        "resources": "- [ggplot2 Elegant Graphics for Data Analysis](https://ggplot2-book.org/)",
        "quiz": [
            {"question": "What is the core function to initialize a plot in ggplot2?", "options": ["ggplot()", "plot()", "ggpoint()", "geom()"], "correct": 0},
            {"question": "How are layers combined in a ggplot2 call?", "options": ["Using the + operator", "Using pipes (%>%)", "By nesting arguments", "Using commas"], "correct": 0},
            {"question": "Which geom adds a scatter plot layer?", "options": ["geom_point()", "geom_scatter()", "geom_dot()", "geom_line()"], "correct": 0}
        ]
    },
    {
        "title": "Session 5: Hypothesis Testing in R",
        "slug": "r-session-5-hypothesis-testing",
        "description": "Formulate statistical claims and compute t-tests in R.",
        "duration": "60 min",
        "difficulty": "Beginner",
        "objectives": """- Define null and alternative hypotheses
- Run one-sample and two-sample t-tests using base R
- Read t-test outputs and extract p-values""",
        "expected_outcomes": """- Set up hypotheses.
- Execute t.test() on numeric columns.
- Evaluate p-values against significance thresholds (alpha=0.05).""",
        "learning_notes": """### t-tests in R
We compare group means to population norms or control treatments:
- `t.test(x, mu=val)`: One-sample t-test.
- `t.test(x, y)`: Independent two-sample t-test.
If the p-value is smaller than alpha (usually 0.05), we reject the null hypothesis.""",
        "instructions": "Execute the R script to run a t-test and compute significance.",
        "content": "Verify experimental differences statistically using t-tests.",
        "code_examples": """# Student scores sample
scores <- c(78, 85, 92, 88, 79, 81, 95, 87)
# Run one-sample t-test
test_result <- t.test(scores, mu=80)
print(test_result)
print(paste("P-value:", test_result$p.value))""",
        "resources": "- [Quick-R t-tests](https://www.statmethods.net/stats/ttests.html)",
        "quiz": [
            {"question": "Which base R function performs a t-test?", "options": ["t.test()", "ttest()", "t_test()", "stats.ttest()"], "correct": 0},
            {"question": "How do you extract the p-value from a t-test result object?", "options": ["result$p.value", "result$pvalue", "p_value(result)", "result$p_val"], "correct": 0},
            {"question": "What is the typical alpha significance limit?", "options": ["0.05", "0.01 only", "0.10", "0.50"], "correct": 0}
        ]
    },
    {
        "title": "Session 6: Correlation and Regression Analysis in R",
        "slug": "r-session-6-correlation-regression",
        "description": "Compute Pearson correlation and fit linear regression models.",
        "duration": "75 min",
        "difficulty": "Beginner",
        "objectives": """- Measure association with cor() and cor.test()
- Fit simple linear models using lm()
- Extract slope, intercept, and R-squared metrics""",
        "expected_outcomes": """- Calculate Pearson's r.
- Fit regression lines.
- Summarize coefficients using summary().""",
        "learning_notes": """### Correlation & Regression
- `cor(x, y)`: Returns the Pearson correlation coefficient.
- `lm(formula, data)`: Fits a linear model. The formula is written as `y ~ x`.
Extract model statistics using `summary(model)`.""",
        "instructions": "Run the regression model code to find intercept and slope parameters.",
        "content": "Predict outcomes and trace associations with linear regression models.",
        "code_examples": """# Correlation and Regression
hours <- c(2, 4, 6, 8, 10)
scores <- c(55, 65, 75, 80, 95)
corr <- cor(hours, scores)
print(paste("Correlation:", corr))
model <- lm(scores ~ hours)
print(summary(model))""",
        "resources": "- [Linear Models in R](https://www.r-bloggers.com/2016/01/fitting-a-least-squares-regression-line-in-r/)",
        "quiz": [
            {"question": "Which function computes correlation in R?", "options": ["cor()", "correlation()", "pearson()", "lm_cor()"], "correct": 0},
            {"question": "How do you define a regression formula of y on x in lm()?", "options": ["y ~ x", "y = x", "x ~ y", "lm(y, x)"], "correct": 0},
            {"question": "Which function returns regression statistics like R-squared?", "options": ["summary()", "coef()", "lm_stats()", "print()"], "correct": 0}
        ]
    },
    {
        "title": "Session 7: ANOVA and Non-Parametric Tests in R",
        "slug": "r-session-7-anova-tests",
        "description": "Compare multiple groups with aov() and Kruskal-Wallis tests.",
        "duration": "75 min",
        "difficulty": "Beginner",
        "objectives": """- Run One-Way ANOVA tests using aov()
- Run post-hoc checks with TukeyHSD()
- Implement Kruskal-Wallis non-parametric tests""",
        "expected_outcomes": """- Test differences across three or more categories.
- Run Tukey multiple comparisons.
- Perform non-parametric tests when assumptions fail.""",
        "learning_notes": """### ANOVA in R
Use `aov(Score ~ Method, data=df)` to perform Analysis of Variance. Follow up significant ANOVA results with `TukeyHSD()` to find specific group differences.
If normality assumptions are violated, use `kruskal.test()`.""",
        "instructions": "Execute the ANOVA and Tukey test scripts to find significant cohort variations.",
        "content": "Compare multiple population segments simultaneously and analyze variance.",
        "code_examples": """# Group data frame
df <- data.frame(
  Method = factor(c(rep("A", 4), rep("B", 4), rep("C", 4))),
  Score = c(85, 88, 90, 82, 72, 75, 80, 78, 91, 95, 88, 92)
)
# Perform ANOVA
fit <- aov(Score ~ Method, data=df)
print(summary(fit))""",
        "resources": "- [ANOVA in R Tutorial](https://www.datanovia.com/en/lessons/anova-in-r/)",
        "quiz": [
            {"question": "Which function is standard for ANOVA in R?", "options": ["aov()", "anova()", "lm_anova()", "compare_means()"], "correct": 0},
            {"question": "What post-hoc test compares all pairwise means after a significant ANOVA?", "options": ["TukeyHSD()", "t.test()", "kruskal.test()", "pairwise.t.test()"], "correct": 0},
            {"question": "Which non-parametric test replaces ANOVA in R?", "options": ["kruskal.test()", "wilcox.test()", "chisq.test()", "aov()"], "correct": 0}
        ]
    },
    {
        "title": "Session 8: Time Series Analysis in R",
        "slug": "r-session-8-time-series",
        "description": "Build ts objects, analyze seasonal patterns, and plot decompositions.",
        "duration": "75 min",
        "difficulty": "Beginner",
        "objectives": """- Convert vectors into time series using ts()
- Decompose series into trend, seasonal, and random parts
- Fit simple moving averages and exponential smoothing""",
        "expected_outcomes": """- Build ts time-frequency objects.
- Plot decompositions with decompose().
- Compute forecasts.""",
        "learning_notes": """### Time Series in R
- `ts(data, start, frequency)`: Declares a time series object.
- `decompose()`: Breaks a series into trend, seasonal, and random components.
Plot components instantly with `plot(decompose(ts_object))`.""",
        "instructions": "Run the time-series setup to construct a simulated quarterly time series object.",
        "content": "Decompose time variables and isolate quarterly trends.",
        "code_examples": """# Simulated quarterly sales data over 2 years
sales <- c(100, 120, 110, 150, 105, 125, 115, 160)
# Create ts object starting in 2023
ts_sales <- ts(sales, start=c(2023, 1), frequency=4)
print(ts_sales)
# Decompose
fit <- decompose(ts_sales, type="additive")
print("Decomposition completed successfully.")""",
        "resources": "- [Time Series Analysis with R](https://otexts.com/fpp2/)",
        "quiz": [
            {"question": "Which function creates a time series object in R?", "options": ["ts()", "timeseries()", "as.ts()", "zoo()"], "correct": 0},
            {"question": "What does frequency=12 indicate in ts()?", "options": ["Monthly data", "Quarterly data", "Weekly data", "Annual data"], "correct": 0},
            {"question": "Which function decomposes a time series into seasonal and trend segments?", "options": ["decompose()", "ts_decompose()", "split_series()", "forecast()"], "correct": 0}
        ]
    },
    {
        "title": "Session 9: Reporting with R Markdown",
        "slug": "r-session-9-r-markdown",
        "description": "Construct dynamic reports that blend text explanations with executed R chunks.",
        "duration": "60 min",
        "difficulty": "Beginner",
        "objectives": """- Structure R Markdown (.Rmd) documents with YAML headers
- Control code chunk display (echo, eval, warning, message)
- Knit documents to HTML, PDF, or Word formats""",
        "expected_outcomes": """- Build R Markdown reports.
- Control chunk rendering settings.
- Produce formatted client summaries.""",
        "learning_notes": """### R Markdown
R Markdown files combine text (in Markdown format) with embedded R code chunks.
Chunks are marked by:
```
{r}
# R code goes here
```
Use `knitr` to build the document, executing all code chunks and inserting their outputs directly into the final report.""",
        "instructions": "Run the R code to generate a text report summary.",
        "content": "Create reproducible document reports that update automatically when new data is added.",
        "code_examples": """# Simulate dynamic report generation
student_count <- 150
passing_pct <- 94.2
report <- paste(
  "--- CDAM ACADEMIC REPORT ---",
  paste("Total Students Evaluated:", student_count),
  paste("Curriculum Completion Rate:", passing_pct, "%"),
  "Recommendation: Advance to Machine Learning module.",
  sep = "\\n"
)
cat(report)""",
        "resources": "- [R Markdown Cookbook](https://bookdown.org/yihui/rmarkdown-cookbook/)",
        "quiz": [
            {"question": "What extension do R Markdown source files use?", "options": [".Rmd", ".R", ".md", ".rmarkdown"], "correct": 0},
            {"question": "Which chunk option prevents R code from being shown in the output?", "options": ["echo = FALSE", "eval = FALSE", "include = FALSE", "results = 'hide'"], "correct": 0},
            {"question": "What is the process of generating the final document from an Rmd file called?", "options": ["Knitting", "Compiling", "Rendering", "Building"], "correct": 0}
        ]
    },
    {
        "title": "Session 10: Capstone Project",
        "slug": "r-session-10-capstone-beginner",
        "description": "Incorporate data cleaning, manipulation, and plotting into a single R pipeline.",
        "duration": "90 min",
        "difficulty": "Beginner",
        "objectives": """- Combine EDA, cleaning, and dplyr operations in one script
- Draw inferences from statistical comparisons
- Present final insights in a structured format""",
        "expected_outcomes": """- Build an end-to-end data pipeline.
- Clean and analyze multi-class performance parameters.
- Output aggregate stats.""",
        "learning_notes": """### Capstone Integration
Bring together everything you've learned: data frame instantiation, dplyr aggregation verbs, stats, plotting, and reporting.""",
        "instructions": "Execute the R code to run the capstone performance pipeline.",
        "content": "Confirm your beginner track mastery by executing this complete R analysis pipeline.",
        "code_examples": """library(dplyr)
# Capstone Simulation
df <- data.frame(
  ID = 1:4,
  Level = c("Beginner", "Beginner", "Advanced", "Advanced"),
  Score = c(85, 78, 92, 88)
)
summary <- df %>% group_by(Level) %>% summarize(MeanScore = mean(Score))
print("CDAM Capstone Executive Summary:")
print(summary)""",
        "resources": "- [CDAM R Portal](https://cdam.chuka.ac.ke/grad/r/)",
        "quiz": [
            {"question": "What is the first step of a reproducible data pipeline?", "options": ["Importing the data", "Modeling variables", "Plotting correlations", "Generating a report"], "correct": 0},
            {"question": "Which dplyr verb aggregates values?", "options": ["summarize()", "filter()", "arrange()", "select()"], "correct": 0},
            {"question": "What package is the foundation of data manipulation in R?", "options": ["dplyr", "ggplot2", "tidyr", "readr"], "correct": 0}
        ]
    },
    {
        "title": "Session 11: Advanced Data Wrangling with tidyr and dplyr",
        "slug": "r-session-11-advanced-wrangling",
        "description": "Reshape data frames and handle complex table joins.",
        "duration": "60 min",
        "difficulty": "Professional",
        "objectives": """- Perform inner, left, right, and full joins with dplyr
- Pivot tables between wide and long layouts using tidyr
- Separate and unite composite columns""",
        "expected_outcomes": """- Join data frames on key variables.
- Reshape tables with pivot_longer() and pivot_wider().
- Clean composite variables.""",
        "learning_notes": """### tidyr & Joins
- `left_join()`, `right_join()`, `inner_join()`, `full_join()`: Combine tables.
- `pivot_longer()`: Convert wide tables (multiple columns) to long format.
- `pivot_wider()`: Convert long tables back to wide format.""",
        "instructions": "Run the pivot code to see wide data pivoted into a long layout.",
        "content": "Reshape, merge, and clean complex tables for advanced analytics.",
        "code_examples": """library(tidyr)
library(dplyr)
# Create wide data
wide_data <- data.frame(
  Year = c(2023, 2024),
  HR_Expense = c(50000, 52000),
  IT_Expense = c(75000, 80000)
)
# Reshape to long format
long_data <- wide_data %>%
  pivot_longer(cols = ends_with("Expense"), names_to = "Dept", values_to = "Expense")
print("Long Format:")
print(long_data)""",
        "resources": "- [tidyr Cheat Sheet](https://github.com/rstudio/cheatsheets/blob/main/data-import.pdf)",
        "quiz": [
            {"question": "Which tidyr function reshapes data from wide to long?", "options": ["pivot_longer()", "pivot_wider()", "gather()", "spread()"], "correct": 0},
            {"question": "Which join preserves all rows in the left table?", "options": ["left_join()", "right_join()", "inner_join()", "full_join()"], "correct": 0},
            {"question": "How do you split a composite column into two columns?", "options": ["separate()", "unite()", "split()", "mutate()"], "correct": 0}
        ]
    },
    {
        "title": "Session 12: Functional Programming in R (purrr / apply family)",
        "slug": "r-session-12-functional-programming",
        "description": "Optimize loops using vectorization, the apply family, and purrr map functions.",
        "duration": "60 min",
        "difficulty": "Professional",
        "objectives": """- Avoid slow for loops using vectorized calculations
- Apply functions across margins using apply, sapply, and lapply
- Build robust iterations using the purrr package""",
        "expected_outcomes": """- Replace manual loops with map() functions.
- Run functions over lists and data frame columns.
- Standardize output types with map_double() or map_chr().""",
        "learning_notes": """### Functional Iteration
In R, loops can be slow and hard to read. Instead, use vectorization or map functions:
- `lapply()`, `sapply()`: Base R loop-replacements.
- `purrr::map()`: Tidyverse iteration returning a list.
- `purrr::map_dbl()`: Iteration guaranteed to return a numeric vector.""",
        "instructions": "Execute the iteration code to square numeric vectors without using loops.",
        "content": "Write clean, fast, and testable code using R functional programming.",
        "code_examples": """library(purrr)
# Vector of inputs
numbers <- 1:10
# Square even numbers using map and filter equivalents
squared_evens <- numbers %>%
  keep(~ .x %% 2 == 0) %>%
  map_dbl(~ .x^2)
print("Squared Evens:")
print(squared_evens)""",
        "resources": "- [Functional Programming with purrr](https://r4ds.had.co.nz/iteration.html)",
        "quiz": [
            {"question": "Which purrr function maps and guarantees a numeric double vector output?", "options": ["map_dbl()", "map()", "map_chr()", "map_num()"], "correct": 0},
            {"question": "What is the base R equivalent of map returning a list?", "options": ["lapply()", "sapply()", "apply()", "mapply()"], "correct": 0},
            {"question": "Which verb filters elements in purrr?", "options": ["keep()", "filter()", "discard()", "select()"], "correct": 0}
        ]
    },
    {
        "title": "Session 13: Advanced Data Visualization with ggplot2",
        "slug": "r-session-13-advanced-visualization",
        "description": "Build multi-panel grids, color scales, and custom themes for publication.",
        "duration": "75 min",
        "difficulty": "Professional",
        "objectives": """- Use facet_wrap and facet_grid to split panels by variables
- Customize color gradients and discrete color palettes
- Build bespoke theme templates for academic or corporate guidelines""",
        "expected_outcomes": """- Build faceted charts.
- Configure color mappings.
- Design theme layouts.""",
        "learning_notes": """### ggplot2 Customization
- `facet_wrap(~ variable)`: Splits plots into multiple panels based on a categorical variable.
- `theme()`: Allows customizing text sizes, backgrounds, legend coordinates, and gridlines.
- `scale_color_manual()`: Enforces custom hex palettes.""",
        "instructions": "Run the plotting script to inspect a simulated faceted chart structure.",
        "content": "Create publication-quality graphic panels matching design requirements.",
        "code_examples": """library(ggplot2)
# Prepare data
df <- data.frame(
  Hours = c(2, 5, 7, 8),
  FinalExam = c(55, 72, 88, 92),
  Group = c("A", "A", "B", "B")
)
# Build faceted plot
p <- ggplot(df, aes(x=Hours, y=FinalExam, color=Group)) +
  geom_point(size=3) +
  facet_wrap(~Group) +
  theme_bw()
print("Faceted plot structured successfully.")""",
        "resources": "- [ggplot2 Themes Gallery](https://ggplot2.org/)",
        "quiz": [
            {"question": "Which function splits plots into separate panels based on a variable?", "options": ["facet_wrap()", "split_plot()", "grid_layout()", "panel_wrap()"], "correct": 0},
            {"question": "How do you customize individual chart elements like legend placement?", "options": ["theme()", "labs()", "scale_legend()", "options()"], "correct": 0},
            {"question": "Which package provides pre-defined themes like theme_economist()?", "options": ["ggthemes", "ggplot2", "scales", "gridExtra"], "correct": 0}
        ]
    },
    {
        "title": "Session 14: Statistical Modeling in R (Multiple Regression)",
        "slug": "r-session-14-statistical-modeling",
        "description": "Fit multiple regression models, evaluate residuals, and diagnose collinearity.",
        "duration": "75 min",
        "difficulty": "Professional",
        "objectives": """- Fit multivariate models using lm(y ~ x1 + x2)
- Read ANOVA tables and interpret multi-predictor coefficients
- Inspect model assumptions using plot(model)""",
        "expected_outcomes": """- Construct multiple regression models.
- Interpret coefficient estimates and R-squared.
- Diagnose model assumptions (homoscedasticity, normality).""",
        "learning_notes": """### Multiple Linear Regression
We model y on multiple predictors:
`model <- lm(y ~ x1 + x2, data=df)`
Interpret results:
- **p-value**: Assesses significance of individual predictors.
- **R-squared**: Goodness-of-fit.
- **Residual plots**: Check for heteroscedasticity or non-normality.""",
        "instructions": "Execute the multiple linear model to check model coefficients.",
        "content": "Estimate relationships using multivariate statistical models.",
        "code_examples": """# Fit multiple predictors model
df <- data.frame(
  Hours = c(2, 4, 6, 8, 10),
  Practice = c(60, 70, 85, 90, 95),
  Exam = c(50, 60, 70, 80, 95)
)
model <- lm(Exam ~ Hours + Practice, data=df)
print(summary(model))""",
        "resources": "- [Regression Diagnostics in R](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/lm.html)",
        "quiz": [
            {"question": "How do you add multiple predictors in lm()?", "options": ["lm(y ~ x1 + x2)", "lm(y ~ x1, x2)", "lm(y ~ x1 & x2)", "lm(y ~ x1 * x2)"], "correct": 0},
            {"question": "Which command generates standard diagnostics plots for lm models?", "options": ["plot(model)", "diagnose(model)", "check(model)", "summary(model)"], "correct": 0},
            {"question": "What does a high VIF (Variance Inflation Factor) indicate?", "options": ["High multicollinearity", "Homoscedasticity", "High accuracy", "High model fit"], "correct": 0}
        ]
    },
    {
        "title": "Session 15: Machine Learning in R (Supervised Learning)",
        "slug": "r-session-15-supervised-learning",
        "description": "Train classification models and measure prediction accuracy.",
        "duration": "75 min",
        "difficulty": "Professional",
        "objectives": """- Split data frames into train and test sets in R
- Train Logistic Regression models using glm()
- Compute confusion matrices, accuracy, and F1 metrics""",
        "expected_outcomes": """- Build train/test partition splits.
- Train glm() classification models.
- Predict and evaluate class outcomes.""",
        "learning_notes": """### Logistic Regression in R
For binary classification, use Generalized Linear Models:
`model <- glm(y ~ x, data=df, family="binomial")`
Generate probability predictions with `predict(model, newdata, type="response")`.""",
        "instructions": "Execute the logistic classifier code to fit and predict test outcomes.",
        "content": "Build R pipelines to classify records and evaluate accuracy.",
        "code_examples": """# Logistic classification
df <- data.frame(
  Hours = c(2, 1, 5, 8, 9),
  Passed = c(0, 0, 0, 1, 1)
)
# Train binomial logistic model
model <- glm(Passed ~ Hours, data=df, family="binomial")
probs <- predict(model, newdata=data.frame(Hours=6), type="response")
print(paste("Probability for 6 hours:", probs))""",
        "resources": "- [caret Package Documentation](https://topepo.github.io/caret/)",
        "quiz": [
            {"question": "Which family parameter is specified in glm() for binary logistic regression?", "options": ["'binomial'", "'gaussian'", "'poisson'", "'logistic'"], "correct": 0},
            {"question": "What parameter is required in predict() to get probabilities instead of log-odds?", "options": ["type = 'response'", "type = 'prob'", "type = 'class'", "probabilities = TRUE"], "correct": 0},
            {"question": "What package is standard for building machine learning pipelines in R?", "options": ["caret", "ggplot2", "dplyr", "tidyr"], "correct": 0}
        ]
    },
    {
        "title": "Session 16: Unsupervised Learning in R",
        "slug": "r-session-16-unsupervised-learning",
        "description": "Cluster unlabeled datasets using K-Means and simplify features with PCA.",
        "duration": "75 min",
        "difficulty": "Professional",
        "objectives": """- Run K-means clustering using kmeans()
- Perform Principal Component Analysis with prcomp()
- Select cluster numbers using the elbow method""",
        "expected_outcomes": """- Cluster observations.
- Run PCA using prcomp().
- Plot variables along principal component axes.""",
        "learning_notes": """### Unsupervised Learning
- `kmeans(data, centers)`: Cluster data.
- `prcomp(data, scale.=TRUE)`: Runs Principal Component Analysis, scaling variables to unit variance.""",
        "instructions": "Run the clustering script to output centers and coordinates.",
        "content": "Discover patterns in unlabeled datasets using R clustering algorithms.",
        "code_examples": """# Cluster sample
X <- matrix(c(1, 2, 1, 4, 1, 0, 10, 2, 10, 4, 10, 0), ncol=2, byrow=TRUE)
# Perform K-Means
fit <- kmeans(X, centers=2)
print("Cluster Centers:")
print(fit$centers)
print("Cluster Assignments:")
print(fit$cluster)""",
        "resources": "- [PCA in R Tutorial](https://www.r-bloggers.com/2021/05/principal-component-analysis-pca-in-r/)",
        "quiz": [
            {"question": "Which function runs K-Means clustering in R?", "options": ["kmeans()", "k_means()", "cluster()", "prcomp()"], "correct": 0},
            {"question": "Which base R function runs Principal Component Analysis?", "options": ["prcomp()", "pca()", "princomp()", "kmeans()"], "correct": 0},
            {"question": "Why is scaling variables important in PCA?", "options": ["To prevent columns with large scales from dominating", "To speed up calculation", "To center the output around zero", "To remove NA values"], "correct": 0}
        ]
    },
    {
        "title": "Session 17: Working with Web Data (httr / jsonlite)",
        "slug": "r-session-17-web-data",
        "description": "Fetch REST API records using httr and parse JSON datasets using jsonlite.",
        "duration": "60 min",
        "difficulty": "Professional",
        "objectives": """- Send GET requests with httr::GET
- Parse JSON payloads with jsonlite::fromJSON
- Convert nested lists into clean Tidyverse tibbles""",
        "expected_outcomes": """- Retrieve HTTP data feeds.
- Convert JSON strings into data frames.
- Connect R scripts to external web APIs.""",
        "learning_notes": """### Web APIs & JSON in R
- `httr::GET(url)`: Fetches online payloads.
- `jsonlite::fromJSON(txt)`: Converts JSON strings directly into R lists or data frames.""",
        "instructions": "Run the script to parse a simulated JSON API server response.",
        "content": "Connect your R session to remote APIs and databases.",
        "code_examples": """library(jsonlite)
# Simulating a JSON API payload response
json_response <- '{"status": "success", "data": {"users": [{"name": "AI Coach", "role": "Tutor"}]}}'
parsed <- fromJSON(json_response)
print("API Response Status:")
print(parsed$status)
print("Coach Name:")
print(parsed$data$users$name)""",
        "resources": "- [jsonlite Vignette](https://cran.r-project.org/web/packages/jsonlite/vignettes/json-apis.html)",
        "quiz": [
            {"question": "Which function parses JSON strings into R structures?", "options": ["fromJSON()", "parse_json()", "read_json()", "json_parse()"], "correct": 0},
            {"question": "Which package is commonly used for HTTP requests in R?", "options": ["httr", "jsonlite", "xml2", "curl"], "correct": 0},
            {"question": "What structure is usually returned by fromJSON() for tabular data?", "options": ["data.frame", "list", "vector", "matrix"], "correct": 0}
        ]
    },
    {
        "title": "Session 18: R Packages and Reproducibility (renv)",
        "slug": "r-session-18-reproducibility",
        "description": "Track dependencies and restore environments with renv.",
        "duration": "60 min",
        "difficulty": "Professional",
        "objectives": """- Initialize renv for projects using renv::init()
- Save package lockfiles with renv::snapshot()
- Restore library settings with renv::restore()""",
        "expected_outcomes": """- Build isolated package libraries.
- Snapshot project dependencies.
- Enforce reproducible packages.""",
        "learning_notes": """### renv & Reproducibility in R
The `renv` package manages private project libraries, locking specific versions of packages like ggplot2 or dplyr to guarantee your analysis works on any computer:
- `renv::init()`: Sets up the project environment.
- `renv::snapshot()`: Saves installed packages to a `renv.lock` file.
- `renv::restore()`: Re-installs packages listed in the lockfile.""",
        "instructions": "Execute the R code to write out a simulated package lockfile manifest.",
        "content": "Lock package versions to guarantee statistical reproducibility.",
        "code_examples": """# Simulated R package manifest
manifest <- list(
  R_version = "4.3.1",
  packages = list(dplyr = "1.1.2", ggplot2 = "3.4.2", tidyr = "1.3.0")
)
print("CDAM R Environment Manifest:")
print(manifest$packages)""",
        "resources": "- [renv Official Guide](https://rstudio.github.io/renv/articles/renv.html)",
        "quiz": [
            {"question": "Which R package is standard for virtual environments?", "options": ["renv", "devtools", "usethis", "packrat"], "correct": 0},
            {"question": "Which function saves installed packages to a lockfile?", "options": ["renv::snapshot()", "renv::init()", "renv::save()", "renv::restore()"], "correct": 0},
            {"question": "How do you restore a project's packages from a lockfile?", "options": ["renv::restore()", "renv::install()", "renv::load()", "renv::init()"], "correct": 0}
        ]
    }
]

