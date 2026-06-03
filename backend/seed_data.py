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
