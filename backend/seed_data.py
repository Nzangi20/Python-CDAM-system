"""Course seed data for CDAM Python for Data Science and Machine Learning.
Defines 18 comprehensive sessions:
- Sessions 1-10: Introduction to Python for Data Science (Beginner)
- Sessions 11-18: Master Python for Data Science and Machine Learning (Professional)
"""

SESSIONS = [
    {
        "title": "Session 1: Introduction to Python Jupyter Notebook and Basic Data Types",
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
        "quiz": []
    },
    {
        "title": "Session 2: Data Importation, Cleaning, and Exploratory Data Analysis",
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
        "quiz": []
    },
    {
        "title": "Session 3: Data Manipulation in Python",
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
        "quiz": []
    },
    {
        "title": "Session 4: Data Visualization with Matplotlib and Seaborn Libraries",
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
        "quiz": []
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
        "quiz": []
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
        "quiz": []
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
        "quiz": []
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
        "quiz": []
    },
    {
        "title": "Session 9: Data Visualization with PyGWalker in Python",
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
        "quiz": []
    },
    {
        "title": "Session 10: Capstone Project in Python",
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
        "quiz": []
    },
    {
        "title": "Session 11: Python Essentials",
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
        "quiz": []
    },
    {
        "title": "Session 12: Numerical and Tabular Computing with NumPy and Pandas",
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
        "quiz": []
    },
    {
        "title": "Session 13: Advanced Data Visualization in Python",
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
        "quiz": []
    },
    {
        "title": "Session 14: Machine Learning Fundamentals with Scikit-Learn",
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
        "quiz": []
    },
    {
        "title": "Session 15: Supervised Learning – Classification",
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
        "quiz": []
    },
    {
        "title": "Session 16: Supervised Learning – Regression",
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
        "quiz": []
    },
    {
        "title": "Session 17: Unsupervised Learning – K-Means and PCA",
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
        "quiz": []
    },
    {
        "title": "Session 18: Capstone Project in Python",
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
        "quiz": []
    }
]

R_SESSIONS = [   {   'code_examples': '# Declare variables in R\n'
                         'name <- "CDAM Student"\n'
                         'age <- 20\n'
                         'gpa <- 3.8\n'
                         'print(paste("Student:", name, "Age:", age, "GPA:", gpa))\n'
                         'print(class(name))\n'
                         'print(class(age))',
        'content': 'Get comfortable writing basic R syntax, assigning variables, and checking their types.',
        'description': 'Learn the fundamentals of R programming, RStudio IDE, and the core concepts of data science.',
        'difficulty': 'Beginner',
        'duration': '45 min',
        'expected_outcomes': '- Declare variables in R using the assignment operator (<-).\n'
                             '- Identify vector classes (numeric, character, logical).\n'
                             '- Run basic math operations on vectors.',
        'instructions': 'Run the code editor cell to calculate variable values and print their class.',
        'learning_notes': '### R & RStudio Overview\n'
                          'R is a programming language specifically built for statistical computing and graphics. '
                          'RStudio is the standard IDE for R.\n'
                          '\n'
                          '### Assignment Operator\n'
                          'In R, we typically use `<-` instead of `=` for assignment:\n'
                          '`x <- 10`\n'
                          '\n'
                          '### Core Data Types\n'
                          '- `numeric`: Decimals or integers (e.g., 3.14, 42)\n'
                          '- `character`: Text strings wrapped in quotes\n'
                          '- `logical`: TRUE or FALSE values (can be abbreviated as T or F)',
        'notes_file_path': 'https://019f40c2-09d4-fb31-50b0-e79ca532e49e.share.connect.posit.cloud/',
        'objectives': '- Set up R and understand the RStudio workspace layout\n'
                      '- Understand variables, vectors, and basic numeric, character, and logical data types\n'
                      '- Execute print statements and run simple calculations in R console',
        'quiz': [],
        'resources': '- [R Manuals](https://cran.r-project.org/manuals.html)\n'
                     '- [RStudio Desktop](https://posit.co/download/rstudio-desktop/)',
        'slug': 'r-session-1-intro-to-r',
        'title': 'Session 1: Introduction to R for Data Science'},
    {   'code_examples': '# Create a sample data frame with NA values\n'
                         'df <- data.frame(\n'
                         '  Name = c("Alice", "Bob", "Carol", NA),\n'
                         '  Age = c(25, NA, 30, 22)\n'
                         ')\n'
                         'print("Original Data Frame:")\n'
                         'print(df)\n'
                         'df_clean <- na.omit(df)\n'
                         'print("Cleaned Data Frame:")\n'
                         'print(df_clean)',
        'content': "Clean datasets using R's built-in functions before starting analysis.",
        'description': 'Master data importation, cleaning techniques, and exploratory data analysis to prepare '
                       'datasets for analysis.',
        'difficulty': 'Beginner',
        'duration': '50 min',
        'expected_outcomes': '- Load a CSV file into an R data.frame.\n'
                             '- Detect missing entries with is.na().\n'
                             '- Filter out rows containing missing values.',
        'instructions': 'Execute the R code to see how rows containing NA values are filtered from a data frame.',
        'learning_notes': '### Exploratory Data Analysis in R\n'
                          'We begin by inspecting data structures using `str()` and calculating summary stats using '
                          '`summary()`.\n'
                          '\n'
                          '### Missing Data (NA)\n'
                          'In R, missing values are represented by `NA`. We use `is.na(x)` to find them, and '
                          '`na.omit()` to drop rows containing any NAs.',
        'notes_file_path': 'https://019f40cd-56e7-ef68-cdd0-fbffbf783050.share.connect.posit.cloud/',
        'objectives': '- Read CSV files using base R read.csv\n'
                      '- Identify missing values (NA) in data frames\n'
                      '- Clean missing values using na.omit and basic imputation',
        'quiz': [],
        'resources': '- [R Data Import/Export Guide](https://cran.r-project.org/doc/manuals/r-release/R-data.html)',
        'slug': 'r-session-2-data-import-eda',
        'title': 'Session 2: Data Import, Cleaning and EDA'},
    {   'code_examples': 'library(dplyr)\n'
                         '# Create sales data\n'
                         'df <- data.frame(\n'
                         '  Region = c("East", "West", "East", "West"),\n'
                         '  Revenue = c(100, 150, 200, 300)\n'
                         ')\n'
                         '# Filter and summarize\n'
                         'east_only <- df %>% filter(Region == "East")\n'
                         'print("East Region only:")\n'
                         'print(east_only)\n'
                         'grouped <- df %>% group_by(Region) %>% summarize(Total = sum(Revenue))\n'
                         'print("Grouped Revenue:")\n'
                         'print(grouped)',
        'content': 'Master dplyr to write readable, elegant data pipelines in R.',
        'description': 'Learn powerful data manipulation techniques using dplyr to transform and organize your data '
                       'efficiently.',
        'difficulty': 'Beginner',
        'duration': '60 min',
        'expected_outcomes': '- Slice and subset data frames using dplyr verbs.\n'
                             '- Compute average scores for categories.\n'
                             '- Chain multiple operations using pipe syntax.',
        'instructions': 'Run the dplyr script to filter sales data and aggregate revenue statistics.',
        'learning_notes': '### dplyr Manipulation\n'
                          'The `dplyr` package is the core tool of the Tidyverse for data manipulation:\n'
                          '- `filter()`: Keep rows matching criteria.\n'
                          '- `select()`: Pick columns by name.\n'
                          '- `mutate()`: Create or transform columns.\n'
                          '- `summarize()`: Aggregate values.\n'
                          '\n'
                          '### Pipe Operator\n'
                          'The pipe operator `%>%` passes the result of one function as the first argument of the '
                          'next.',
        'notes_file_path': 'https://019f40d2-7d76-1343-15a2-638e763635bf.share.connect.posit.cloud/',
        'objectives': '- Understand tidyverse and the pipe operator (%>% or |>)\n'
                      '- Use dplyr verbs: filter, select, mutate, and arrange\n'
                      '- Perform group summaries using group_by and summarize',
        'quiz': [],
        'resources': '- [dplyr Cheatsheet](https://github.com/rstudio/cheatsheets/blob/main/data-transformation.pdf)',
        'slug': 'r-session-3-dplyr-manipulation',
        'title': 'Session 3: Data Manipulation with dplyr'},
    {   'code_examples': 'library(ggplot2)\n'
                         '# Prepare data\n'
                         'df <- data.frame(\n'
                         '  Hours = c(1, 2, 3, 4),\n'
                         '  Score = c(10, 20, 25, 30)\n'
                         ')\n'
                         '# Construct line chart\n'
                         'p <- ggplot(df, aes(x=Hours, y=Score)) +\n'
                         '  geom_line(color="red") +\n'
                         '  geom_point(color="blue", size=3) +\n'
                         '  theme_minimal() +\n'
                         '  labs(title="Performance Chart", x="Hours", y="Score")\n'
                         'print("Plot structured successfully!")',
        'content': 'Create rich, multi-layered visual charts using ggplot2.',
        'description': 'Create professional, publication-quality graphics using ggplot2 and the Grammar of Graphics.',
        'difficulty': 'Beginner',
        'duration': '60 min',
        'expected_outcomes': '- Build charts using ggplot() and geom functions.\n'
                             '- Customize colors and labels.\n'
                             '- Save charts using ggsave().',
        'instructions': 'Execute the ggplot code to set up a sample line chart.',
        'learning_notes': '### ggplot2 & Grammar of Graphics\n'
                          'ggplot2 is built on the Grammar of Graphics, combining data, aesthetic mappings (`aes`), '
                          'and geometric layers (`geom_`):\n'
                          '- `geom_point()`: Scatter plots.\n'
                          '- `geom_line()`: Line charts.\n'
                          '- `geom_bar()`: Bar charts.',
        'notes_file_path': 'https://019f40d7-71c6-36e8-2d30-e50a254eb4f9.share.connect.posit.cloud/',
        'objectives': '- Understand the layers of the Grammar of Graphics\n'
                      '- Create scatter plots, bar charts, and line plots with ggplot\n'
                      '- Customize themes, colors, and axis labels',
        'quiz': [],
        'resources': '- [ggplot2 Elegant Graphics for Data Analysis](https://ggplot2-book.org/)',
        'slug': 'r-session-4-ggplot2-visualization',
        'title': 'Session 4: Data Visualization with ggplot2'},
    {   'code_examples': '# Student scores sample\n'
                         'scores <- c(78, 85, 92, 88, 79, 81, 95, 87)\n'
                         '# Run one-sample t-test\n'
                         'test_result <- t.test(scores, mu=80)\n'
                         'print(test_result)\n'
                         'print(paste("P-value:", test_result$p.value))',
        'content': 'Verify experimental differences statistically using t-tests.',
        'description': 'Learn statistical hypothesis testing methods including t-tests, chi-square tests, and '
                       'correlation analysis.',
        'difficulty': 'Beginner',
        'duration': '60 min',
        'expected_outcomes': '- Set up hypotheses.\n'
                             '- Execute t.test() on numeric columns.\n'
                             '- Evaluate p-values against significance thresholds (alpha=0.05).',
        'instructions': 'Execute the R script to run a t-test and compute significance.',
        'learning_notes': '### t-tests in R\n'
                          'We compare group means to population norms or control treatments:\n'
                          '- `t.test(x, mu=val)`: One-sample t-test.\n'
                          '- `t.test(x, y)`: Independent two-sample t-test.\n'
                          'If the p-value is smaller than alpha (usually 0.05), we reject the null hypothesis.',
        'notes_file_path': 'https://019f40da-5e17-a6e6-580a-2b22194e2728.share.connect.posit.cloud/',
        'objectives': '- Define null and alternative hypotheses\n'
                      '- Run one-sample and two-sample t-tests using base R\n'
                      '- Read t-test outputs and extract p-values',
        'quiz': [],
        'resources': '- [Quick-R t-tests](https://www.statmethods.net/stats/ttests.html)',
        'slug': 'r-session-5-hypothesis-testing',
        'title': 'Session 5: Hypothesis Testing'},
    {   'code_examples': '# Correlation and Regression\n'
                         'hours <- c(2, 4, 6, 8, 10)\n'
                         'scores <- c(55, 65, 75, 80, 95)\n'
                         'corr <- cor(hours, scores)\n'
                         'print(paste("Correlation:", corr))\n'
                         'model <- lm(scores ~ hours)\n'
                         'print(summary(model))',
        'content': 'Predict outcomes and trace associations with linear regression models.',
        'description': 'Master correlation analysis and regression modeling to understand and predict relationships '
                       'between variables.',
        'difficulty': 'Beginner',
        'duration': '75 min',
        'expected_outcomes': "- Calculate Pearson's r.\n"
                             '- Fit regression lines.\n'
                             '- Summarize coefficients using summary().',
        'instructions': 'Run the regression model code to find intercept and slope parameters.',
        'learning_notes': '### Correlation & Regression\n'
                          '- `cor(x, y)`: Returns the Pearson correlation coefficient.\n'
                          '- `lm(formula, data)`: Fits a linear model. The formula is written as `y ~ x`.\n'
                          'Extract model statistics using `summary(model)`.',
        'notes_file_path': 'https://019f40dc-ff38-1995-58a7-a986fc1eb9aa.share.connect.posit.cloud/',
        'objectives': '- Measure association with cor() and cor.test()\n'
                      '- Fit simple linear models using lm()\n'
                      '- Extract slope, intercept, and R-squared metrics',
        'quiz': [],
        'resources': '- [Linear Models in '
                     'R](https://www.r-bloggers.com/2016/01/fitting-a-least-squares-regression-line-in-r/)',
        'slug': 'r-session-6-correlation-regression',
        'title': 'Session 6: Correlation and Regression Analysis'},
    {   'code_examples': '# Group data frame\n'
                         'df <- data.frame(\n'
                         '  Method = factor(c(rep("A", 4), rep("B", 4), rep("C", 4))),\n'
                         '  Score = c(85, 88, 90, 82, 72, 75, 80, 78, 91, 95, 88, 92)\n'
                         ')\n'
                         '# Perform ANOVA\n'
                         'fit <- aov(Score ~ Method, data=df)\n'
                         'print(summary(fit))',
        'content': 'Compare multiple population segments simultaneously and analyze variance.',
        'description': 'Extend your statistical testing toolkit with Analysis of Variance (ANOVA) and non-parametric '
                       'alternatives.',
        'difficulty': 'Beginner',
        'duration': '75 min',
        'expected_outcomes': '- Test differences across three or more categories.\n'
                             '- Run Tukey multiple comparisons.\n'
                             '- Perform non-parametric tests when assumptions fail.',
        'instructions': 'Execute the ANOVA and Tukey test scripts to find significant cohort variations.',
        'learning_notes': '### ANOVA in R\n'
                          'Use `aov(Score ~ Method, data=df)` to perform Analysis of Variance. Follow up significant '
                          'ANOVA results with `TukeyHSD()` to find specific group differences.\n'
                          'If normality assumptions are violated, use `kruskal.test()`.',
        'notes_file_path': 'https://019f40e0-0802-97af-4580-c6dee929895a.share.connect.posit.cloud/',
        'objectives': '- Run One-Way ANOVA tests using aov()\n'
                      '- Run post-hoc checks with TukeyHSD()\n'
                      '- Implement Kruskal-Wallis non-parametric tests',
        'quiz': [],
        'resources': '- [ANOVA in R Tutorial](https://www.datanovia.com/en/lessons/anova-in-r/)',
        'slug': 'r-session-7-anova-tests',
        'title': 'Session 7: ANOVA and Non-Parametric Tests'},
    {   'code_examples': '# Simulated quarterly sales data over 2 years\n'
                         'sales <- c(100, 120, 110, 150, 105, 125, 115, 160)\n'
                         '# Create ts object starting in 2023\n'
                         'ts_sales <- ts(sales, start=c(2023, 1), frequency=4)\n'
                         'print(ts_sales)\n'
                         '# Decompose\n'
                         'fit <- decompose(ts_sales, type="additive")\n'
                         'print("Decomposition completed successfully.")',
        'content': 'Decompose time variables and isolate quarterly trends.',
        'description': 'Master time series analysis techniques for forecasting and trend analysis.',
        'difficulty': 'Beginner',
        'duration': '75 min',
        'expected_outcomes': '- Build ts time-frequency objects.\n'
                             '- Plot decompositions with decompose().\n'
                             '- Compute forecasts.',
        'instructions': 'Run the time-series setup to construct a simulated quarterly time series object.',
        'learning_notes': '### Time Series in R\n'
                          '- `ts(data, start, frequency)`: Declares a time series object.\n'
                          '- `decompose()`: Breaks a series into trend, seasonal, and random components.\n'
                          'Plot components instantly with `plot(decompose(ts_object))`.',
        'notes_file_path': 'https://019f4142-087e-cf54-f225-1f6c1d12382b.share.connect.posit.cloud/',
        'objectives': '- Convert vectors into time series using ts()\n'
                      '- Decompose series into trend, seasonal, and random parts\n'
                      '- Fit simple moving averages and exponential smoothing',
        'quiz': [],
        'resources': '- [Time Series Analysis with R](https://otexts.com/fpp2/)',
        'slug': 'r-session-8-time-series',
        'title': 'Session 8: Time Series Analysis'},
    {   'code_examples': 'library(dplyr)\n'
                         '# Capstone Simulation\n'
                         'df <- data.frame(\n'
                         '  ID = 1:4,\n'
                         '  Level = c("Beginner", "Beginner", "Advanced", "Advanced"),\n'
                         '  Score = c(85, 78, 92, 88)\n'
                         ')\n'
                         'summary <- df %>% group_by(Level) %>% summarize(MeanScore = mean(Score))\n'
                         'print("CDAM Capstone Executive Summary:")\n'
                         'print(summary)',
        'content': 'Confirm your beginner track mastery by executing this complete R analysis pipeline.',
        'description': 'Apply all your R data science skills to real-world capstone projects.',
        'difficulty': 'Beginner',
        'duration': '90 min',
        'expected_outcomes': '- Build an end-to-end data pipeline.\n'
                             '- Clean and analyze multi-class performance parameters.\n'
                             '- Output aggregate stats.',
        'instructions': 'Execute the R code to run the capstone performance pipeline.',
        'learning_notes': '### Capstone Integration\n'
                          "Bring together everything you've learned: data frame instantiation, dplyr aggregation "
                          'verbs, stats, plotting, and reporting.',
        'notes_file_path': 'https://019f413a-2978-f27d-2314-c298cdb340e7.share.connect.posit.cloud/',
        'objectives': '- Combine EDA, cleaning, and dplyr operations in one script\n'
                      '- Draw inferences from statistical comparisons\n'
                      '- Present final insights in a structured format',
        'quiz': [],
        'resources': '- [CDAM R Portal](https://cdam.chuka.ac.ke/grad/r/)',
        'slug': 'r-session-9-capstone',
        'title': 'Session 9: Capstone Projects'},
    {   'code_examples': '',
        'content': 'Intermediate to advanced statistical modeling and regression analysis.',
        'description': 'Deep dive into statistical modeling, regression techniques, and predictive analysis.',
        'difficulty': 'Professional',
        'duration': '60 min',
        'expected_outcomes': '',
        'instructions': '',
        'learning_notes': '',
        'notes_file_path': None,
        'objectives': '',
        'quiz': [],
        'resources': '',
        'slug': 'r-session-10',
        'title': 'Session 10: Session Ten'},
    {   'code_examples': '',
        'content': 'Master advanced functional programming concepts using tidyverse tools.',
        'description': 'Advanced data transformation, nesting, and functional programming with purrr.',
        'difficulty': 'Professional',
        'duration': '60 min',
        'expected_outcomes': '',
        'instructions': '',
        'learning_notes': '',
        'notes_file_path': None,
        'objectives': '',
        'quiz': [],
        'resources': '',
        'slug': 'r-session-11',
        'title': 'Session 11: Session Eleven'},
    {   'code_examples': '',
        'content': 'Implement classification models and inspect performance metrics in R.',
        'description': 'Supervised machine learning algorithms, classification models, and model evaluation.',
        'difficulty': 'Professional',
        'duration': '75 min',
        'expected_outcomes': '',
        'instructions': '',
        'learning_notes': '',
        'notes_file_path': None,
        'objectives': '',
        'quiz': [],
        'resources': '',
        'slug': 'r-session-12',
        'title': 'Session 12: Session Twelve'},
    {   'code_examples': '',
        'content': 'Discover patterns in unlabeled datasets using clustering and PCA reduction.',
        'description': 'Unsupervised learning, clustering algorithms (K-means), and dimension reduction (PCA).',
        'difficulty': 'Professional',
        'duration': '75 min',
        'expected_outcomes': '',
        'instructions': '',
        'learning_notes': '',
        'notes_file_path': None,
        'objectives': '',
        'quiz': [],
        'resources': '',
        'slug': 'r-session-13',
        'title': 'Session 13: Session Thirteen'},
    {   'code_examples': '',
        'content': 'Train basic deep learning networks and optimize parameters.',
        'description': 'Deep learning foundations, neural networks, and advanced tensor operations in R.',
        'difficulty': 'Professional',
        'duration': '90 min',
        'expected_outcomes': '',
        'instructions': '',
        'learning_notes': '',
        'notes_file_path': None,
        'objectives': '',
        'quiz': [],
        'resources': '',
        'slug': 'r-session-14',
        'title': 'Session 14: Session Fourteen'},
    {   'code_examples': '',
        'content': 'Extract topics and perform sentiments analysis on textual corpora.',
        'description': 'Natural language processing (NLP), text mining, and sentiment analysis with tidytext.',
        'difficulty': 'Professional',
        'duration': '90 min',
        'expected_outcomes': '',
        'instructions': '',
        'learning_notes': '',
        'notes_file_path': None,
        'objectives': '',
        'quiz': [],
        'resources': '',
        'slug': 'r-session-15',
        'title': 'Session 15: Session Fifteen'},
    {   'code_examples': '',
        'content': 'Combine ML/AI capabilities into a final R capstone project.',
        'description': 'Capstone project integration, final model deployments, and system reporting.',
        'difficulty': 'Professional',
        'duration': '120 min',
        'expected_outcomes': '',
        'instructions': '',
        'learning_notes': '',
        'notes_file_path': None,
        'objectives': '',
        'quiz': [],
        'resources': '',
        'slug': 'r-session-16',
        'title': 'Session 16: Session Sixteen'}]
