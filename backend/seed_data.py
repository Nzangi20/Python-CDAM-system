"""Course seed data for CDAM Python for Data Science and Machine Learning.
Defines 18 comprehensive sessions:
- Sessions 1-10: Introduction to Python for Data Science (Beginner)
- Sessions 11-18: Master Python for Data Science and Machine Learning (Professional)
"""

SESSIONS = [   {   'code_examples': '# Declare variables and print types\n'
                         'name = "CDAM Student"\n'
                         'age = 20\n'
                         'gpa = 3.8\n'
                         'print(f"Student: {name}, Age: {age}, GPA: {gpa}")\n'
                         'print(type(name), type(age), type(gpa))',
        'content': 'This session introduces learners to Python programming using Jupyter Notebook. Participants learn '
                   'how to navigate the notebook environment, write and execute Python code, and understand '
                   'fundamental data types used in programming and data analysis.',
        'description': 'Get started with Python syntax, Jupyter Notebook environment, and core variables.',
        'difficulty': 'Beginner',
        'duration': '45 min',
        'expected_outcomes': '- Navigate and use Jupyter Notebook effectively.\n'
                             '- Write and execute simple Python programs.\n'
                             "- Work confidently with Python's basic data types.\n"
                             '- Apply basic programming concepts to solve simple problems.',
        'instructions': 'Run the code editor cell to calculate variable values and print their types.',
        'learning_notes': '### Python & Jupyter Overview\n'
                          'Python is a general-purpose programming language popular for its readability. Jupyter '
                          'Notebooks allow you to mix markdown explanations with executable python code blocks in a '
                          'web browser.\n'
                          '\n'
                          '### Primitive Types\n'
                          '- `int`: Integers (e.g. 5, -12)\n'
                          '- `float`: Decimals (e.g. 3.14, 0.0)\n'
                          '- `str`: Text wrapped in single or double quotes\n'
                          '- `bool`: True or False value',
        'objectives': '- Understand the Python programming language and its applications.\n'
                      '- Install and navigate the Jupyter Notebook environment.\n'
                      '- Learn Python syntax and coding conventions.\n'
                      '- Identify and use basic data types including integers, floats, strings, and booleans.\n'
                      '- Perform basic input, output, and arithmetic operations.',
        'quiz': [],
        'resources': '- [Python Official Tutorial](https://docs.python.org/3/tutorial/)\\n- [Jupyter Notebook '
                     'Docs](https://jupyter-notebook.readthedocs.io/)',
        'slug': 'session-1-intro-to-python-jupyter',
        'title': 'Session 1: Introduction to Python, Jupyter Notebook and Basic Data Types'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Import and clean a sample dataset\n'
                         "data = {'Name': ['Alice', 'Bob', 'Carol', None], 'Age': [25, None, 30, 22]}\n"
                         'df = pd.DataFrame(data)\n'
                         'print("Original:")\n'
                         'print(df)\n'
                         'df_clean = df.dropna()\n'
                         'print("\\nCleaned:")\n'
                         'print(df_clean)',
        'content': 'This session focuses on acquiring datasets, cleaning inconsistent data, and performing exploratory '
                   'data analysis (EDA) to understand data characteristics before analysis.',
        'description': 'Learn how to read CSV files, locate missing values, and execute basic cleaning operations.',
        'difficulty': 'Beginner',
        'duration': '50 min',
        'expected_outcomes': '- Import datasets into Python successfully.\n'
                             '- Clean and prepare datasets for analysis.\n'
                             '- Perform exploratory data analysis.\n'
                             '- Summarize key insights from data.',
        'instructions': 'Execute the pandas code to see how rows containing Null or None values are deleted from the '
                        'DataFrame.',
        'learning_notes': '### Exploratory Data Analysis (EDA)\n'
                          'EDA is the initial phase of data analysis where you inspect summary stats, detect outliers, '
                          'and check completeness.\n'
                          '\n'
                          '### Cleaning Techniques\n'
                          '- `dropna()`: Remove rows or columns containing missing values.\n'
                          '- `fillna()`: Replace missing values with static values or calculated column means.',
        'objectives': '- Import datasets from various file formats.\n'
                      '- Handle missing values and duplicate records.\n'
                      '- Detect and correct data inconsistencies.\n'
                      '- Generate descriptive statistics.\n'
                      '- Explore datasets using visualization techniques.',
        'quiz': [],
        'resources': '- [Pandas IO Docs](https://pandas.pydata.org/docs/user_guide/io.html)',
        'slug': 'session-2-data-import-eda',
        'title': 'Session 2: Data Importation, Cleaning, and Exploratory Data Analysis'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Filter and aggregate data\n'
                         "sales = {'Region': ['East', 'West', 'East', 'West'], 'Revenue': [100, 150, 200, 300]}\n"
                         'df = pd.DataFrame(sales)\n'
                         "east_only = df[df['Region'] == 'East']\n"
                         'print("East Only:")\n'
                         'print(east_only)\n'
                         'print("\\nGrouped Revenue:")\n'
                         "print(df.groupby('Region').sum())",
        'content': 'This session introduces techniques for organizing, filtering, transforming, and combining datasets '
                   'using Pandas.',
        'description': 'Filter columns, select rows by condition, and group statistics with pandas.',
        'difficulty': 'Beginner',
        'duration': '60 min',
        'expected_outcomes': '- Manipulate datasets efficiently.\n'
                             '- Apply transformations to data.\n'
                             '- Prepare datasets for statistical analysis.\n'
                             '- Perform data aggregation tasks.',
        'instructions': 'Run the code to filter the sample sales data and compute aggregated sum metrics.',
        'learning_notes': '### Data Manipulation\n'
                          "DataFrames represent tables. We filter using boolean expressions (e.g. `df[df['Score'] > "
                          '80]`). Grouping merges rows based on a target category and applies aggregate operations '
                          'like `.sum()`, `.mean()`, or `.count()`.',
        'objectives': '- Select and filter data.\n'
                      '- Sort datasets.\n'
                      '- Merge and concatenate datasets.\n'
                      '- Group and aggregate data.\n'
                      '- Create and modify columns.',
        'quiz': [],
        'resources': '- [Pandas Indexing Tutorial](https://pandas.pydata.org/docs/user_guide/indexing.html)',
        'slug': 'session-3-pandas-data-manipulation',
        'title': 'Session 3: Data Manipulation in Python'},
    {   'code_examples': 'import matplotlib.pyplot as plt\n'
                         '# Plot simple line chart\n'
                         'x = [1, 2, 3, 4]\n'
                         'y = [10, 20, 25, 30]\n'
                         "plt.plot(x, y, marker='o', color='red')\n"
                         'plt.title("Sample Performance Chart")\n'
                         'plt.xlabel("Hours Studied")\n'
                         'plt.ylabel("Score")\n'
                         'print("Chart ready for rendering!")',
        'content': 'Learners explore graphical techniques for presenting data using Matplotlib and Seaborn.',
        'description': 'Create charts, customize axes labels, and build visual heatmaps for presentations.',
        'difficulty': 'Beginner',
        'duration': '60 min',
        'expected_outcomes': '- Produce informative data visualizations.\n'
                             '- Customize charts professionally.\n'
                             '- Communicate findings visually.\n'
                             '- Interpret trends and patterns.',
        'instructions': 'Generate and print confirmation of chart building using the code cell.',
        'learning_notes': '### Data Visualization\n'
                          'Visualizations help communicate trends.\n'
                          '- `matplotlib.pyplot` is the core library for plotting.\n'
                          '- `seaborn` provides higher-level aesthetic defaults built on top of matplotlib.',
        'objectives': '- Create line, bar, histogram, scatter, and box plots.\n'
                      '- Customize visualizations.\n'
                      '- Select appropriate charts for different data types.\n'
                      '- Interpret graphical outputs.',
        'quiz': [],
        'resources': '- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)\\n- [Seaborn '
                     'Tutorial](https://seaborn.pydata.org/tutorial.html)',
        'slug': 'session-4-matplotlib-seaborn-viz',
        'title': 'Session 4: Data Visualization with Matplotlib and Seaborn Libraries'},
    {   'code_examples': 'import scipy.stats as stats\n'
                         '# Perform a one-sample t-test\n'
                         'scores = [78, 85, 92, 88, 79, 81, 95, 87]\n'
                         't_stat, p_val = stats.ttest_1samp(scores, popmean=80)\n'
                         'print(f"T-statistic: {t_stat:.4f}")\n'
                         'print(f"P-value: {p_val:.4f}")',
        'content': 'This session introduces statistical hypothesis testing for making evidence-based decisions.',
        'description': 'Learn statistical inference: define null hypotheses and compute p-values.',
        'difficulty': 'Beginner',
        'duration': '60 min',
        'expected_outcomes': '- Conduct hypothesis tests.\n'
                             '- Interpret statistical significance.\n'
                             '- Draw valid conclusions from data.\n'
                             '- Report hypothesis testing results accurately.',
        'instructions': 'Execute the t-test on student scores to calculate the t-statistic and the p-value.',
        'learning_notes': '### Hypothesis Testing\n'
                          'Hypothesis tests verify if a sample observation differs significantly from a population '
                          'mean or control group.\n'
                          '- **Null Hypothesis (H0)**: No effect or no difference.\n'
                          '- **P-value**: Probability of getting results at least as extreme, assuming H0 is true. If '
                          'p < 0.05, we reject H0.',
        'objectives': '- Understand null and alternative hypotheses.\n'
                      '- Perform common statistical tests.\n'
                      '- Interpret p-values.\n'
                      '- Make statistical decisions.',
        'quiz': [],
        'resources': '- [SciPy Stats Tutorial](https://docs.scipy.org/doc/scipy/tutorial/stats.html)',
        'slug': 'session-5-hypothesis-testing',
        'title': 'Session 5: Hypothesis Testing'},
    {   'code_examples': 'import numpy as np\n'
                         'import scipy.stats as stats\n'
                         '# Correlation between study hours and exam scores\n'
                         'hours = [2, 4, 6, 8, 10]\n'
                         'scores = [55, 65, 75, 80, 95]\n'
                         'corr, p = stats.pearsonr(hours, scores)\n'
                         'slope, intercept, r, p_val, std_err = stats.linregress(hours, scores)\n'
                         'print(f"Correlation Coefficient: {corr:.4f}")\n'
                         'print(f"Regression Line: y = {slope:.2f}x + {intercept:.2f}")',
        'content': 'Participants learn how variables relate to each other and how regression models predict outcomes.',
        'description': 'Measure associations between variables and build linear models.',
        'difficulty': 'Beginner',
        'duration': '75 min',
        'expected_outcomes': '- Measure relationships between variables.\n'
                             '- Build regression models.\n'
                             '- Interpret predictive models.\n'
                             '- Evaluate regression accuracy.',
        'instructions': 'Run the code to calculate both correlation and linear regression parameters.',
        'learning_notes': '### Correlation vs Causation\n'
                          "Correlation measures strength and direction of linear association. Pearson's r values range "
                          'from -1 to 1.\n'
                          'Linear regression computes:\n'
                          '`y = slope * x + intercept`\n'
                          'It represents the line of best fit through the data points.',
        'objectives': '- Understand correlation coefficients.\n'
                      '- Perform simple linear regression.\n'
                      '- Interpret regression outputs.\n'
                      '- Evaluate model performance.',
        'quiz': [],
        'resources': '- [SciPy linregress '
                     'Docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html)',
        'slug': 'session-6-correlation-regression',
        'title': 'Session 6: Correlation and Regression Analysis'},
    {   'code_examples': 'import scipy.stats as stats\n'
                         '# One-way ANOVA test for three study methods\n'
                         'method_A = [85, 88, 90, 82]\n'
                         'method_B = [72, 75, 80, 78]\n'
                         'method_C = [91, 95, 88, 92]\n'
                         'f_stat, p_val = stats.f_oneway(method_A, method_B, method_C)\n'
                         'print(f"F-statistic: {f_stat:.4f}")\n'
                         'print(f"P-value: {p_val:.4f}")',
        'content': 'This session covers statistical methods used to compare multiple groups and analyze data that '
                   'violate parametric assumptions.',
        'description': 'Compare multiple means with ANOVA and check categorical counts with Chi-square.',
        'difficulty': 'Beginner',
        'duration': '75 min',
        'expected_outcomes': '- Compare group means effectively.\n'
                             '- Conduct non-parametric tests.\n'
                             '- Interpret ANOVA results.\n'
                             '- Choose appropriate statistical methods.',
        'instructions': 'Run the code to perform a One-Way ANOVA test on three sample education methods.',
        'learning_notes': '### ANOVA (Analysis of Variance)\n'
                          'ANOVA compares the means of three or more independent groups to see if at least one group '
                          'mean is statistically different.\n'
                          'If normality assumptions are violated, use non-parametric tests like Kruskal-Wallis.',
        'objectives': '- Understand ANOVA principles.\n'
                      '- Perform one-way ANOVA.\n'
                      '- Learn non-parametric alternatives.\n'
                      '- Interpret statistical outputs.',
        'quiz': [],
        'resources': '- [ANOVA on Wikipedia](https://en.wikipedia.org/wiki/Analysis_of_variance)',
        'slug': 'session-7-anova-tests',
        'title': 'Session 7: Analysis of Variance (ANOVA) and Non-Parametric Tests'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Time series index and rolling mean\n'
                         'dates = pd.date_range(start="2024-01-01", periods=5, freq="D")\n'
                         'values = [100, 105, 98, 110, 115]\n'
                         'ts = pd.Series(values, index=dates)\n'
                         'print("Time Series:")\n'
                         'print(ts)\n'
                         'print("\\n2-Day Rolling Mean:")\n'
                         'print(ts.rolling(window=2).mean())',
        'content': 'Learners explore techniques for analyzing data collected over time to identify trends and '
                   'patterns.',
        'description': 'Understand date indexes, resample time logs, and compute rolling moving averages.',
        'difficulty': 'Beginner',
        'duration': '75 min',
        'expected_outcomes': '- Analyze temporal datasets.\n'
                             '- Visualize time series data.\n'
                             '- Identify time-based patterns.\n'
                             '- Develop basic forecasting models.',
        'instructions': 'Execute the code to create a date-indexed series and calculate a moving average.',
        'learning_notes': '### Time Series Data\n'
                          'A time series is a sequence of observations taken sequentially in time.\n'
                          '- `resample()`: Aggregates time frequencies (e.g. sum daily logs into weekly totals).\n'
                          '- `rolling()`: Calculates statistics in a moving window, smoothing out noise.',
        'objectives': '- Understand time series concepts.\n'
                      '- Prepare time-indexed datasets.\n'
                      '- Identify trends and seasonality.\n'
                      '- Generate simple forecasts.',
        'quiz': [],
        'resources': '- [Pandas Time Series Guide](https://pandas.pydata.org/docs/user_guide/timeseries.html)',
        'slug': 'session-8-time-series',
        'title': 'Session 8: Time Series Analysis'},
    {   'code_examples': '# Simulate generating a report summary\n'
                         'student_count = 150\n'
                         'passing_pct = 94.2\n'
                         "report = f'''\n"
                         '--- CDAM ACADEMIC REPORT ---\n'
                         'Total Students Evaluated: {student_count}\n'
                         'Curriculum Completion Rate: {passing_pct}%\n'
                         'Recommendation: Advance to Professional module.\n'
                         "'''\n"
                         'print(report)',
        'content': 'This session introduces PyGWalker for interactive, no-code data exploration and visualization.',
        'description': 'Generate clean reports, insert markdown explanations, and configure notebook layouts.',
        'difficulty': 'Beginner',
        'duration': '60 min',
        'expected_outcomes': '- Build interactive visualizations.\n'
                             '- Explore data efficiently.\n'
                             '- Create dashboards without extensive coding.\n'
                             '- Present findings effectively.',
        'instructions': 'Run the cell to generate a simulated executive academic report summary.',
        'learning_notes': '### Notebook Reports\n'
                          'Jupyter Notebook is not just a coding console — it is a document tool.\n'
                          'Use markdown headings (`#`, `##`, `###`) to structure sections and write key findings to '
                          'support numerical analytics results.',
        'objectives': '- Install and configure PyGWalker.\n'
                      '- Explore datasets interactively.\n'
                      '- Generate dashboards.\n'
                      '- Interpret interactive visualizations.',
        'quiz': [],
        'resources': '- [Jupyter Markdown Guide](https://www.markdownguide.org/tools/jupyter-notebook/)',
        'slug': 'session-9-jupyter-reporting',
        'title': 'Session 9: Data Visualization with PyGWalker in Python'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Beginner Capstone Simulation\n'
                         '# Perform full flow: Import -> Clean -> Group -> Output Statistics\n'
                         "raw_data = {'ID': [1, 2, 3, 4], 'Level': ['Beginner', 'Beginner', 'Advanced', 'Advanced'], "
                         "'Score': [85, 78, 92, 88]}\n"
                         'df = pd.DataFrame(raw_data)\n'
                         "summary = df.groupby('Level')['Score'].mean()\n"
                         'print("CDAM Capstone Executive Summary:")\n'
                         'print(summary)',
        'content': 'Participants apply skills learned in previous sessions to complete an end-to-end data analysis '
                   'project.',
        'description': 'Demonstrate your data skills: import, clean, analyze, and present a sample dataset.',
        'difficulty': 'Beginner',
        'duration': '90 min',
        'expected_outcomes': '- Complete a comprehensive Python project.\n'
                             '- Demonstrate data analysis skills.\n'
                             '- Produce professional reports.\n'
                             '- Communicate analytical insights.',
        'instructions': 'Execute the capstone simulation code to analyze multi-level student performances.',
        'learning_notes': '### Capstone Integration\n'
                          'The capstone combines everything you have learned in the Beginner course: basic variables, '
                          'cleaning, grouping, statistical analysis, and markdown presentation of results.',
        'objectives': '- Import and prepare data.\n'
                      '- Analyze datasets.\n'
                      '- Visualize findings.\n'
                      '- Present project results.',
        'quiz': [],
        'resources': '- [CDAM Graduation Portal](https://cdam.chuka.ac.ke/grad/)',
        'slug': 'session-10-capstone-beginner',
        'title': 'Session 10: Capstone Project in Python'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Analyze Agricultural Crop Production (ML) Dataset\n'
                         "data = {'Crop': ['Maize', 'Wheat', 'Rice', 'Beans', 'Maize', 'Wheat'], 'Yield_kg_ha': [2500, "
                         "3200, 4500, 1800, 2700, 3400], 'Rainfall_mm': [800, 750, 1200, 600, 850, 780], "
                         "'Fertilizer_kg_ha': [150, 180, 200, 100, 160, 190]}\n"
                         'df = pd.DataFrame(data)\n'
                         'print("Agricultural Crop Production Data:")\n'
                         'print(df)',
        'content': 'This session reinforces core Python programming concepts necessary for advanced applications, '
                   'using the Agricultural Crop Production (ML) dataset.',
        'description': 'Learn multi-index, merge operations, and pivot tables to reshape complex tables using '
                       'real-world agricultural data.',
        'difficulty': 'Professional',
        'duration': '60 min',
        'expected_outcomes': '- Write efficient Python programs.\n'
                             '- Develop reusable functions.\n'
                             '- Apply control structures effectively.\n'
                             '- Build modular applications using agricultural data.',
        'instructions': 'Execute the pivot table simulation to analyze crop yield metrics from the Agricultural Crop '
                        'Production dataset.',
        'learning_notes': '### Relational Operations & Pivoting\n'
                          'In professional environments, data is split. Use `pd.merge()` to perform database-style '
                          'inner, outer, left, and right joins.\n'
                          '`pivot_table()` builds summary tables similar to Excel pivot tools, grouping metrics by '
                          'multiple indexes.\n'
                          '\n'
                          '### Agricultural Crop Production (ML) Dataset\n'
                          'This dataset contains crop yield data with factors like rainfall and fertilizer '
                          'application, perfect for machine learning modeling.',
        'objectives': '- Review variables and operators.\n'
                      '- Understand functions.\n'
                      '- Apply loops and conditional statements.\n'
                      '- Work with modules and packages.',
        'quiz': [],
        'resources': '- [Pandas Reshaping Documentation](https://pandas.pydata.org/docs/user_guide/reshaping.html)',
        'slug': 'session-11-advanced-pandas',
        'title': 'Session 11: Python Essentials with Agricultural Crop Production Data'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Analyze Customer Banking Transactions (ML) Dataset\n'
                         'data = [\n'
                         '    {"id": 1, "amount": 2500, "type": "deposit"},\n'
                         '    {"id": 2, "amount": 1200, "type": "withdrawal"},\n'
                         '    {"id": 3, "amount": 3000, "type": "deposit"},\n'
                         '    {"id": 4, "amount": 800, "type": "withdrawal"},\n'
                         '    {"id": 5, "amount": 5000, "type": "deposit"}\n'
                         ']\n'
                         'print("Customer Banking Transactions Data:")\n'
                         'for t in data:\n'
                         '    print(t)',
        'content': 'Participants learn efficient numerical computation and structured data manipulation using the '
                   'Customer Banking Transactions (ML) dataset.',
        'description': 'Optimize your loops with lambda, map, filter, and list comprehensions using real-world banking '
                       'transaction data.',
        'difficulty': 'Professional',
        'duration': '60 min',
        'expected_outcomes': '- Perform numerical computations efficiently.\n'
                             '- Analyze structured datasets using banking transaction data.\n'
                             '- Manipulate large datasets.\n'
                             '- Improve data processing performance.',
        'instructions': 'Run the code to compare functional map/filter against clean list comprehensions using the '
                        'Customer Banking Transactions dataset.',
        'learning_notes': '### Functional Programming\n'
                          'Functional styles avoid mutating state.\n'
                          '- `lambda`: Simple inline functions.\n'
                          '- `map(func, iterable)`: Applies a function to all elements.\n'
                          '- `filter(pred, iterable)`: Keeps elements matching a condition.\n'
                          '\n'
                          '### Customer Banking Transactions (ML) Dataset\n'
                          'This dataset contains customer transaction records, perfect for fraud detection and '
                          'customer behavior analysis using machine learning.',
        'objectives': '- Create NumPy arrays.\n'
                      '- Perform numerical operations.\n'
                      '- Manipulate Pandas DataFrames.\n'
                      '- Optimize data processing workflows.',
        'quiz': [],
        'resources': '- [Python Functional Programming HowTo](https://docs.python.org/3/howto/functional.html)',
        'slug': 'session-12-functional-programming',
        'title': 'Session 12: Numerical and Tabular Computing with Customer Banking Transactions Data'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Analyze Retail Sales (ML) Dataset\n'
                         "data = {'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], 'Sales': [5000, 6200, 5800, "
                         "7500, 8000, 7200], 'AdSpend': [500, 650, 600, 800, 850, 750], 'FootTraffic': [1200, 1500, "
                         '1400, 1800, 1900, 1700]}\n'
                         'df = pd.DataFrame(data)\n'
                         'print("Retail Sales Data:")\n'
                         'print(df)',
        'content': 'This session focuses on creating advanced and publication-quality visualizations using the Retail '
                   'Sales (ML) dataset.',
        'description': 'Build multi-panel grids, style correlation matrices, and customize plot settings using '
                       'real-world retail sales data.',
        'difficulty': 'Professional',
        'duration': '75 min',
        'expected_outcomes': '- Produce professional visualizations.\n'
                             '- Communicate complex insights effectively using retail data.\n'
                             '- Develop interactive dashboards.\n'
                             '- Present analytical findings clearly.',
        'instructions': 'Run the code to calculate a correlation matrix for the Retail Sales dataset.',
        'learning_notes': '### Advanced Visualization\n'
                          'For complex analysis, one plot is not enough.\n'
                          'Use `plt.subplots(rows, cols)` to arrange multiple panels.\n'
                          '`seaborn.heatmap()` visualizes correlation tables, making numeric associations clear at a '
                          'glance.\n'
                          '\n'
                          '### Retail Sales (ML) Dataset\n'
                          'This dataset contains monthly sales, ad spend, and foot traffic data, perfect for sales '
                          'prediction and marketing optimization using machine learning.',
        'objectives': '- Build advanced statistical plots.\n'
                      '- Create interactive visualizations.\n'
                      '- Customize layouts and themes.\n'
                      '- Visualize multidimensional data.',
        'quiz': [],
        'resources': '- [Seaborn Heatmap Docs](https://seaborn.pydata.org/generated/seaborn.heatmap.html)',
        'slug': 'session-13-advanced-visualization',
        'title': 'Session 13: Advanced Data Visualization with Retail Sales Data'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Analyze Agricultural Crop Production (ML) Dataset\n'
                         "data = {'Crop': ['Maize', 'Wheat', 'Rice', 'Beans', 'Maize', 'Wheat'], 'Yield_kg_ha': [2500, "
                         "3200, 4500, 1800, 2700, 3400], 'Rainfall_mm': [800, 750, 1200, 600, 850, 780], "
                         "'Fertilizer_kg_ha': [150, 180, 200, 100, 160, 190]}\n"
                         'df = pd.DataFrame(data)\n'
                         'print("Agricultural Crop Production Data:")\n'
                         'print(df)',
        'content': 'Learners are introduced to machine learning concepts and model development using Scikit-Learn. '
                   'using the Agricultural Crop Production (ML) dataset.',
        'description': 'Construct Ordinary Least Squares (OLS) regression models and evaluate p-values. using '
                       'real-world Agricultural Crop Production data.',
        'difficulty': 'Professional',
        'duration': '75 min',
        'expected_outcomes': '- Build introductory machine learning models.\n'
                             '- Apply preprocessing techniques.\n'
                             '- Evaluate model accuracy.\n'
                             '- Understand supervised and unsupervised learning concepts.',
        'instructions': 'Execute the OLS linear model to output the statistical summary table.',
        'learning_notes': '### Ordinary Least Squares (OLS)\n'
                          'OLS regression models the relationship between dependent and independent variables.\n'
                          '- **R-squared**: Percentage of variance in the target explained by the predictors.\n'
                          '- **P>|t|**: P-value checking if predictor coefficients are significantly different from '
                          '0.\n'
                          '\n'
                          '### Agricultural Crop Production (ML)\n'
                          'This dataset contains crop yield data with factors like rainfall and fertilizer '
                          'application, perfect for machine learning modeling.',
        'objectives': '- Understand machine learning workflows.\n'
                      '- Prepare data for modeling.\n'
                      '- Train basic models.\n'
                      '- Evaluate model performance.',
        'quiz': [],
        'resources': '- [Statsmodels OLS Guide](https://www.statsmodels.org/stable/regression.html)',
        'slug': 'session-14-statistical-modeling',
        'title': 'Session 14: Machine Learning Fundamentals with Scikit-Learn with Agricultural Crop Production Data'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Analyze Customer Banking Transactions (ML) Dataset\n'
                         'data = [\n'
                         '    {"id": 1, "amount": 2500, "type": "deposit"},\n'
                         '    {"id": 2, "amount": 1200, "type": "withdrawal"},\n'
                         '    {"id": 3, "amount": 3000, "type": "deposit"},\n'
                         '    {"id": 4, "amount": 800, "type": "withdrawal"},\n'
                         '    {"id": 5, "amount": 5000, "type": "deposit"}\n'
                         ']\n'
                         'print("Customer Banking Transactions Data:")\n'
                         'for t in data:\n'
                         '    print(t)',
        'content': 'This session focuses on building models that predict categorical outcomes. using the Customer '
                   'Banking Transactions (ML) dataset.',
        'description': 'Train linear classifiers, predict classes, and measure model accuracy. using real-world '
                       'Customer Banking Transactions data.',
        'difficulty': 'Professional',
        'duration': '75 min',
        'expected_outcomes': '- Build classification models.\n'
                             '- Predict categorical outcomes.\n'
                             '- Evaluate classification accuracy.\n'
                             '- Select suitable classification algorithms.',
        'instructions': 'Execute the logistic classifier code to fit and predict test outcomes.',
        'learning_notes': '### Supervised Learning\n'
                          'Supervised models learn from labeled pairs.\n'
                          '- **Classification**: Target is categorical (e.g. Pass/Fail, Spam/Ham).\n'
                          '- **Logistic Regression**: Outputs a probability score between 0 and 1, mapped to class '
                          'labels.\n'
                          '\n'
                          '### Customer Banking Transactions (ML)\n'
                          'This dataset contains customer transaction records, perfect for fraud detection and '
                          'customer behavior analysis using machine learning.',
        'objectives': '- Understand classification algorithms.\n'
                      '- Train classification models.\n'
                      '- Evaluate classifier performance.\n'
                      '- Interpret confusion matrices.',
        'quiz': [],
        'resources': '- [Scikit-Learn Supervised Learning '
                     'Guide](https://scikit-learn.org/stable/supervised_learning.html)',
        'slug': 'session-15-supervised-learning',
        'title': 'Session 15: Supervised Learning – Classification with Customer Banking Transactions Data'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Analyze Retail Sales (ML) Dataset\n'
                         "data = {'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], 'Sales': [5000, 6200, 5800, "
                         "7500, 8000, 7200], 'AdSpend': [500, 650, 600, 800, 850, 750], 'FootTraffic': [1200, 1500, "
                         '1400, 1800, 1900, 1700]}\n'
                         'df = pd.DataFrame(data)\n'
                         'print("Retail Sales Data:")\n'
                         'print(df)',
        'content': 'Participants learn regression techniques for predicting continuous numerical values. using the '
                   'Retail Sales (ML) dataset.',
        'description': 'Cluster data with K-Means and simplify columns with Principal Component Analysis. using '
                       'real-world Retail Sales data.',
        'difficulty': 'Professional',
        'duration': '75 min',
        'expected_outcomes': '- Build regression models.\n'
                             '- Predict continuous outcomes.\n'
                             '- Evaluate regression performance.\n'
                             '- Apply regression to real-world problems.',
        'instructions': 'Execute the clustering code to find cluster coordinates and labels.',
        'learning_notes': '### Unsupervised Clustering\n'
                          'Unsupervised algorithms find hidden structures in data without pre-existing labels.\n'
                          '- **K-Means**: Clusters data into K groups based on distances to cluster centers.\n'
                          '- **PCA**: Projects high-dimensional datasets onto principal axes to reduce dimensions '
                          'while saving variance.\n'
                          '\n'
                          '### Retail Sales (ML)\n'
                          'This dataset contains monthly sales, ad spend, and foot traffic data, perfect for sales '
                          'prediction and marketing optimization using machine learning.',
        'objectives': '- Understand regression algorithms.\n'
                      '- Train regression models.\n'
                      '- Evaluate prediction accuracy.\n'
                      '- Compare regression techniques.',
        'quiz': [],
        'resources': '- [Scikit-Learn Clustering Docs](https://scikit-learn.org/stable/modules/clustering.html)',
        'slug': 'session-16-unsupervised-learning',
        'title': 'Session 16: Supervised Learning – Regression with Retail Sales Data'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Analyze Agricultural Crop Production (ML) Dataset\n'
                         "data = {'Crop': ['Maize', 'Wheat', 'Rice', 'Beans', 'Maize', 'Wheat'], 'Yield_kg_ha': [2500, "
                         "3200, 4500, 1800, 2700, 3400], 'Rainfall_mm': [800, 750, 1200, 600, 850, 780], "
                         "'Fertilizer_kg_ha': [150, 180, 200, 100, 160, 190]}\n"
                         'df = pd.DataFrame(data)\n'
                         'print("Agricultural Crop Production Data:")\n'
                         'print(df)',
        'content': 'This session introduces clustering and dimensionality reduction techniques for discovering hidden '
                   'patterns in data. using the Agricultural Crop Production (ML) dataset.',
        'description': 'Fetch remote JSON data from REST APIs and parse database schemas. using real-world '
                       'Agricultural Crop Production data.',
        'difficulty': 'Professional',
        'duration': '60 min',
        'expected_outcomes': '- Cluster similar observations.\n'
                             '- Reduce dataset dimensionality.\n'
                             '- Discover hidden data structures.\n'
                             '- Visualize clustered datasets effectively.',
        'instructions': 'Run the code to simulate parsing a JSON API server payload response.',
        'learning_notes': '### REST APIs & JSON\n'
                          "Much of the world's data is stored in remote servers.\n"
                          'Web APIs return structured text formatted as JSON (JavaScript Object Notation). Use the '
                          'requests library to send HTTP GET calls and unpack dictionary responses.\n'
                          '\n'
                          '### Agricultural Crop Production (ML)\n'
                          'This dataset contains crop yield data with factors like rainfall and fertilizer '
                          'application, perfect for machine learning modeling.',
        'objectives': '- Understand unsupervised learning concepts.\n'
                      '- Apply K-Means clustering.\n'
                      '- Perform Principal Component Analysis (PCA).\n'
                      '- Interpret clustering results.',
        'quiz': [],
        'resources': '- [Python Requests Documentation](https://requests.readthedocs.io/)',
        'slug': 'session-17-external-data-sources',
        'title': 'Session 17: Unsupervised Learning – K-Means and PCA with Agricultural Crop Production Data'},
    {   'code_examples': 'import pandas as pd\n'
                         '# Analyze Customer Banking Transactions (ML) Dataset\n'
                         'data = [\n'
                         '    {"id": 1, "amount": 2500, "type": "deposit"},\n'
                         '    {"id": 2, "amount": 1200, "type": "withdrawal"},\n'
                         '    {"id": 3, "amount": 3000, "type": "deposit"},\n'
                         '    {"id": 4, "amount": 800, "type": "withdrawal"},\n'
                         '    {"id": 5, "amount": 5000, "type": "deposit"}\n'
                         ']\n'
                         'print("Customer Banking Transactions Data:")\n'
                         'for t in data:\n'
                         '    print(t)',
        'content': 'The final session allows participants to integrate all acquired knowledge by solving a '
                   'comprehensive real-world data science problem using Python. using the Customer Banking '
                   'Transactions (ML) dataset.',
        'description': 'Lock package versions, write requirements files, and package reproducible data reports. using '
                       'real-world Customer Banking Transactions data.',
        'difficulty': 'Professional',
        'duration': '60 min',
        'expected_outcomes': '- Successfully complete an end-to-end data science project.\n'
                             '- Demonstrate proficiency in Python for data analysis and machine learning.\n'
                             '- Produce a professional-quality analytical report and presentation.\n'
                             '- Showcase readiness to apply Python data science skills in academic, research, or '
                             'industry settings.',
        'instructions': 'Run the script cell to generate a sample reproducible dependency manifest.',
        'learning_notes': '### Scientific Reproducibility\n'
                          'A study is reproducible if another researcher can run the identical code on the same data '
                          'and get the exact same results.\n'
                          'Always lock package versions (e.g. `pandas==2.1.1`) and enforce seeds in random '
                          'algorithms.\n'
                          '\n'
                          '### Customer Banking Transactions (ML)\n'
                          'This dataset contains customer transaction records, perfect for fraud detection and '
                          'customer behavior analysis using machine learning.',
        'objectives': '- Design a complete data analysis workflow.\n'
                      '- Apply data preprocessing, visualization, statistics, and machine learning techniques.\n'
                      '- Develop and evaluate predictive models where applicable.\n'
                      '- Present findings through reports and visualizations.',
        'quiz': [],
        'resources': '- [Pip Virtual '
                     'Environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)',
        'slug': 'session-18-reporting-reproducibility',
        'title': 'Session 18: Capstone Project in Python with Customer Banking Transactions Data'}]

R_SESSIONS = [{'code_examples': '# Declare variables in R\n'
                   'name <- "CDAM Student"\n'
                   'age <- 20\n'
                   'gpa <- 3.8\n'
                   'print(paste("Student:", name, "Age:", age, "GPA:", gpa))\n'
                   'print(class(name))\n'
                   'print(class(age))',
  'content': 'This session introduces learners to the R programming language and its role in data science. '
             'Participants become familiar with the R environment, RStudio interface, basic syntax, data types, '
             'variables, operators, and fundamental programming concepts used in statistical computing and data '
             'analysis.',
  'description': 'Learn the fundamentals of R programming, RStudio IDE, and the core concepts of data science.',
  'difficulty': 'Beginner',
  'duration': '45 min',
  'expected_outcomes': '- Navigate the RStudio environment confidently.\n'
                       '- Write and execute basic R programs.\n'
                       '- Use R data types and structures effectively.\n'
                       '- Apply fundamental programming concepts to solve simple analytical problems.',
  'instructions': 'Run the code editor cell to calculate variable values and print their class.',
  'learning_notes': '### R & RStudio Overview\n'
                    'R is a programming language specifically built for statistical computing and graphics. RStudio is '
                    'the standard IDE for R.\n'
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
  'objectives': '- Understand the fundamentals of the R programming language.\n'
                '- Install and navigate the R and RStudio environments.\n'
                '- Learn basic R syntax and programming concepts.\n'
                '- Identify and use different data types and data structures in R.\n'
                '- Write and execute simple R scripts.',
  'quiz': [],
  'resources': '- [R Manuals](https://cran.r-project.org/manuals.html)\n'
               '- [RStudio Desktop](https://posit.co/download/rstudio-desktop/)',
  'slug': 'r-session-1-intro-to-r',
  'title': 'Session 1: Introduction to R for Data Science'},
 {'code_examples': '# Create a sample data frame with NA values\n'
                   'df <- data.frame(\n'
                   '  Name = c("Alice", "Bob", "Carol", NA),\n'
                   '  Age = c(25, NA, 30, 22)\n'
                   ')\n'
                   'print("Original Data Frame:")\n'
                   'print(df)\n'
                   'df_clean <- na.omit(df)\n'
                   'print("Cleaned Data Frame:")\n'
                   'print(df_clean)',
  'content': 'This session focuses on importing datasets from various sources, cleaning and preparing data for '
             'analysis, and performing exploratory data analysis to understand data characteristics and identify '
             'patterns.',
  'description': 'Master data importation, cleaning techniques, and exploratory data analysis to prepare datasets for '
                 'analysis.',
  'difficulty': 'Beginner',
  'duration': '50 min',
  'expected_outcomes': '- Successfully import and prepare datasets for analysis.\n'
                       '- Clean datasets using appropriate techniques.\n'
                       '- Perform exploratory data analysis effectively.\n'
                       '- Identify trends, patterns, and potential data quality issues.',
  'instructions': 'Execute the R code to see how rows containing NA values are filtered from a data frame.',
  'learning_notes': '### Exploratory Data Analysis in R\n'
                    'We begin by inspecting data structures using `str()` and calculating summary stats using '
                    '`summary()`.\n'
                    '\n'
                    '### Missing Data (NA)\n'
                    'In R, missing values are represented by `NA`. We use `is.na(x)` to find them, and `na.omit()` to '
                    'drop rows containing any NAs.',
  'notes_file_path': 'https://019f40cd-56e7-ef68-cdd0-fbffbf783050.share.connect.posit.cloud/',
  'objectives': '- Import datasets into R from different file formats.\n'
                '- Handle missing values and duplicate records.\n'
                '- Clean and transform datasets.\n'
                '- Generate descriptive statistics.\n'
                '- Explore datasets using summary tables and visualizations.',
  'quiz': [],
  'resources': '- [R Data Import/Export Guide](https://cran.r-project.org/doc/manuals/r-release/R-data.html)',
  'slug': 'r-session-2-data-import-eda',
  'title': 'Session 2: Data Importation, Cleaning and Exploratory Data Analysis (EDA)'},
 {'code_examples': 'library(dplyr)\n'
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
  'content': 'Participants learn how to manipulate and transform data efficiently using the **dplyr** package, one of '
             'the core tools within the tidyverse ecosystem.',
  'description': 'Learn powerful data manipulation techniques using dplyr to transform and organize your data '
                 'efficiently.',
  'difficulty': 'Beginner',
  'duration': '60 min',
  'expected_outcomes': '- Manipulate datasets efficiently using dplyr.\n'
                       '- Perform data transformation and aggregation.\n'
                       '- Combine datasets from different sources.\n'
                       '- Prepare datasets for statistical analysis and visualization.',
  'instructions': 'Run the dplyr script to filter sales data and aggregate revenue statistics.',
  'learning_notes': '### dplyr Manipulation\n'
                    'The `dplyr` package is the core tool of the Tidyverse for data manipulation:\n'
                    '- `filter()`: Keep rows matching criteria.\n'
                    '- `select()`: Pick columns by name.\n'
                    '- `mutate()`: Create or transform columns.\n'
                    '- `summarize()`: Aggregate values.\n'
                    '\n'
                    '### Pipe Operator\n'
                    'The pipe operator `%>%` passes the result of one function as the first argument of the next.',
  'notes_file_path': 'https://019f40d2-7d76-1343-15a2-638e763635bf.share.connect.posit.cloud/',
  'objectives': '- Select and filter observations.\n'
                '- Arrange and sort datasets.\n'
                '- Create and modify variables.\n'
                '- Group and summarize data.\n'
                '- Join multiple datasets.',
  'quiz': [],
  'resources': '- [dplyr Cheatsheet](https://github.com/rstudio/cheatsheets/blob/main/data-transformation.pdf)',
  'slug': 'r-session-3-dplyr-manipulation',
  'title': 'Session 3: Data Manipulation with dplyr'},
 {'code_examples': 'library(ggplot2)\n'
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
  'content': 'This session introduces learners to creating professional and informative visualizations using the '
             '**ggplot2** package.',
  'description': 'Create professional, publication-quality graphics using ggplot2 and the Grammar of Graphics.',
  'difficulty': 'Beginner',
  'duration': '60 min',
  'expected_outcomes': '- Produce high-quality visualizations.\n'
                       '- Customize graphs for effective communication.\n'
                       '- Present data insights clearly.\n'
                       '- Interpret trends and relationships from visualizations.',
  'instructions': 'Execute the ggplot code to set up a sample line chart.',
  'learning_notes': '### ggplot2 & Grammar of Graphics\n'
                    'ggplot2 is built on the Grammar of Graphics, combining data, aesthetic mappings (`aes`), and '
                    'geometric layers (`geom_`):\n'
                    '- `geom_point()`: Scatter plots.\n'
                    '- `geom_line()`: Line charts.\n'
                    '- `geom_bar()`: Bar charts.',
  'notes_file_path': 'https://019f40d7-71c6-36e8-2d30-e50a254eb4f9.share.connect.posit.cloud/',
  'objectives': '- Understand the Grammar of Graphics.\n'
                '- Create common statistical plots.\n'
                '- Customize charts with themes, labels, and colors.\n'
                '- Select appropriate visualization techniques.\n'
                '- Interpret graphical outputs.',
  'quiz': [],
  'resources': '- [ggplot2 Elegant Graphics for Data Analysis](https://ggplot2-book.org/)',
  'slug': 'r-session-4-ggplot2-visualization',
  'title': 'Session 4: Data Visualization in R with ggplot2'},
 {'code_examples': '# Student scores sample\n'
                   'scores <- c(78, 85, 92, 88, 79, 81, 95, 87)\n'
                   '# Run one-sample t-test\n'
                   'test_result <- t.test(scores, mu=80)\n'
                   'print(test_result)\n'
                   'print(paste("P-value:", test_result$p.value))',
  'content': 'This session introduces statistical hypothesis testing using R to make data-driven decisions based on '
             'sample data.',
  'description': 'Learn statistical hypothesis testing methods including t-tests, chi-square tests, and correlation '
                 'analysis.',
  'difficulty': 'Beginner',
  'duration': '60 min',
  'expected_outcomes': '- Conduct hypothesis testing using R.\n'
                       '- Interpret statistical test results accurately.\n'
                       '- Make evidence-based decisions.\n'
                       '- Report findings in a professional manner.',
  'instructions': 'Execute the R script to run a t-test and compute significance.',
  'learning_notes': '### t-tests in R\n'
                    'We compare group means to population norms or control treatments:\n'
                    '- `t.test(x, mu=val)`: One-sample t-test.\n'
                    '- `t.test(x, y)`: Independent two-sample t-test.\n'
                    'If the p-value is smaller than alpha (usually 0.05), we reject the null hypothesis.',
  'notes_file_path': 'https://019f40da-5e17-a6e6-580a-2b22194e2728.share.connect.posit.cloud/',
  'objectives': '- Understand null and alternative hypotheses.\n'
                '- Perform common hypothesis tests in R.\n'
                '- Interpret p-values and confidence intervals.\n'
                '- Draw statistical conclusions from data.',
  'quiz': [],
  'resources': '- [Quick-R t-tests](https://www.statmethods.net/stats/ttests.html)',
  'slug': 'r-session-5-hypothesis-testing',
  'title': 'Session 5: Hypothesis Testing in R'},
 {'code_examples': '# Correlation and Regression\n'
                   'hours <- c(2, 4, 6, 8, 10)\n'
                   'scores <- c(55, 65, 75, 80, 95)\n'
                   'corr <- cor(hours, scores)\n'
                   'print(paste("Correlation:", corr))\n'
                   'model <- lm(scores ~ hours)\n'
                   'print(summary(model))',
  'content': 'Learners explore statistical techniques for measuring relationships between variables and building '
             'predictive regression models in R.',
  'description': 'Master correlation analysis and regression modeling to understand and predict relationships between '
                 'variables.',
  'difficulty': 'Beginner',
  'duration': '75 min',
  'expected_outcomes': '- Measure relationships between variables.\n'
                       '- Build and interpret regression models.\n'
                       '- Evaluate predictive accuracy.\n'
                       '- Apply regression analysis to real-world datasets.',
  'instructions': 'Run the regression model code to find intercept and slope parameters.',
  'learning_notes': '### Correlation & Regression\n'
                    '- `cor(x, y)`: Returns the Pearson correlation coefficient.\n'
                    '- `lm(formula, data)`: Fits a linear model. The formula is written as `y ~ x`.\n'
                    'Extract model statistics using `summary(model)`.',
  'notes_file_path': 'https://019f40dc-ff38-1995-58a7-a986fc1eb9aa.share.connect.posit.cloud/',
  'objectives': '- Calculate correlation coefficients.\n'
                '- Perform simple linear regression.\n'
                '- Interpret regression coefficients.\n'
                '- Evaluate regression model performance.',
  'quiz': [],
  'resources': '- [Linear Models in '
               'R](https://www.r-bloggers.com/2016/01/fitting-a-least-squares-regression-line-in-r/)',
  'slug': 'r-session-6-correlation-regression',
  'title': 'Session 6: Correlation and Regression Analysis'},
 {'code_examples': '# Group data frame\n'
                   'df <- data.frame(\n'
                   '  Method = factor(c(rep("A", 4), rep("B", 4), rep("C", 4))),\n'
                   '  Score = c(85, 88, 90, 82, 72, 75, 80, 78, 91, 95, 88, 92)\n'
                   ')\n'
                   '# Perform ANOVA\n'
                   'fit <- aov(Score ~ Method, data=df)\n'
                   'print(summary(fit))',
  'content': 'This session covers statistical methods for comparing multiple groups and analyzing datasets that do not '
             'meet the assumptions required for parametric tests.',
  'description': 'Extend your statistical testing toolkit with Analysis of Variance (ANOVA) and non-parametric '
                 'alternatives.',
  'difficulty': 'Beginner',
  'duration': '75 min',
  'expected_outcomes': '- Compare group means effectively.\n'
                       '- Apply appropriate non-parametric tests.\n'
                       '- Interpret statistical significance correctly.\n'
                       '- Select suitable statistical techniques for different data types.',
  'instructions': 'Execute the ANOVA and Tukey test scripts to find significant cohort variations.',
  'learning_notes': '### ANOVA in R\n'
                    'Use `aov(Score ~ Method, data=df)` to perform Analysis of Variance. Follow up significant ANOVA '
                    'results with `TukeyHSD()` to find specific group differences.\n'
                    'If normality assumptions are violated, use `kruskal.test()`.',
  'notes_file_path': 'https://019f40e0-0802-97af-4580-c6dee929895a.share.connect.posit.cloud/',
  'objectives': '- Understand the principles of ANOVA.\n'
                '- Perform one-way ANOVA in R.\n'
                '- Conduct non-parametric statistical tests.\n'
                '- Interpret statistical outputs.',
  'quiz': [],
  'resources': '- [ANOVA in R Tutorial](https://www.datanovia.com/en/lessons/anova-in-r/)',
  'slug': 'r-session-7-anova-tests',
  'title': 'Session 7: Analysis of Variance and Non-Parametric Tests'},
 {'code_examples': '# Simulated quarterly sales data over 2 years\n'
                   'sales <- c(100, 120, 110, 150, 105, 125, 115, 160)\n'
                   '# Create ts object starting in 2023\n'
                   'ts_sales <- ts(sales, start=c(2023, 1), frequency=4)\n'
                   'print(ts_sales)\n'
                   '# Decompose\n'
                   'fit <- decompose(ts_sales, type="additive")\n'
                   'print("Decomposition completed successfully.")',
  'content': 'Participants learn to use **GwalkR**, an interactive visualization package that enables intuitive '
             'exploration and dashboard creation with minimal coding.',
  'description': 'Master time series analysis techniques for forecasting and trend analysis.',
  'difficulty': 'Beginner',
  'duration': '75 min',
  'expected_outcomes': '- Create interactive visualizations.\n'
                       '- Explore large datasets efficiently.\n'
                       '- Develop simple analytical dashboards.\n'
                       '- Communicate findings through interactive visual reports.',
  'instructions': 'Run the time-series setup to construct a simulated quarterly time series object.',
  'learning_notes': '### Time Series in R\n'
                    '- `ts(data, start, frequency)`: Declares a time series object.\n'
                    '- `decompose()`: Breaks a series into trend, seasonal, and random components.\n'
                    'Plot components instantly with `plot(decompose(ts_object))`.',
  'notes_file_path': 'https://019f4142-087e-cf54-f225-1f6c1d12382b.share.connect.posit.cloud/',
  'objectives': '- Install and configure GwalkR.\n'
                '- Explore datasets interactively.\n'
                '- Generate interactive charts and dashboards.\n'
                '- Interpret visual insights obtained from GwalkR.',
  'quiz': [],
  'resources': '- [Time Series Analysis with R](https://otexts.com/fpp2/)',
  'slug': 'r-session-8-time-series',
  'title': 'Session 8: Data Visualization with GwalkR in R'},
 {'code_examples': '# Analyze Agricultural Production Capstone Dataset\n'
                   'data <- data.frame(\n'
                   "  Crop = c('Maize', 'Wheat', 'Rice', 'Beans', 'Maize', 'Wheat'),\n"
                   '  Yield_kg_ha = c(2500, 3200, 4500, 1800, 2700, 3400),\n'
                   '  Rainfall_mm = c(800, 750, 1200, 600, 850, 780),\n'
                   '  Fertilizer_kg_ha = c(150, 180, 200, 100, 160, 190)\n'
                   ')\n'
                   'print("Agricultural Production Capstone Data:")\n'
                   'print(data)',
  'content': 'The final session provides participants with an opportunity to integrate the concepts and techniques '
             'learned throughout the course by completing a comprehensive data science project using R.',
  'description': 'Apply all your R data science skills to real-world capstone projects. using real-world Agricultural '
                 'Production Capstone data.',
  'difficulty': 'Beginner',
  'duration': '90 min',
  'expected_outcomes': '- Successfully complete an end-to-end data science project using R.\n'
                       '- Demonstrate proficiency in R for data analysis and statistical computing.\n'
                       '- Produce professional-quality visualizations, reports, and presentations.\n'
                       '- Showcase readiness to apply R data science skills in academic, research, and industry '
                       'environments.',
  'instructions': 'Execute the R code to run the capstone performance pipeline.',
  'learning_notes': '### Capstone Integration\n'
                    "Bring together everything you've learned: data frame instantiation, dplyr aggregation verbs, "
                    'stats, plotting, and reporting.\n'
                    '\n'
                    '### Agricultural Production Capstone\n'
                    'This dataset contains crop yield data with factors like rainfall and fertilizer application, '
                    'perfect for statistical modeling.',
  'notes_file_path': 'https://019f413a-2978-f27d-2314-c298cdb340e7.share.connect.posit.cloud/',
  'objectives': '- Design and implement a complete data analysis workflow.\n'
                '- Apply data cleaning, manipulation, visualization, and statistical analysis techniques.\n'
                '- Interpret and communicate analytical findings.\n'
                '- Present a professional project report and presentation.',
  'quiz': [],
  'resources': '- [CDAM R Portal](https://cdam.chuka.ac.ke/grad/r/)',
  'slug': 'r-session-9-capstone',
  'title': 'Session 9: Capstone Project in R with Agricultural Production Capstone Data'},
 {'code_examples': 'library(dplyr)\n'
                   'library(tidyr)\n'
                   'library(data.table)\n'
                   '# Reshape and summarize using tidyverse and data.table\n'
                   'df <- data.frame(\n'
                   '  id = 1:4,\n'
                   '  group = c("A", "A", "B", "B"),\n'
                   '  val1 = c(10, 15, 8, 12),\n'
                   '  val2 = c(20, 25, 18, 22)\n'
                   ')\n'
                   '# Pivot longer\n'
                   'df_long <- df %>% pivot_longer(cols = starts_with("val"), names_to = "measure", values_to = '
                   '"value")\n'
                   'print("Reshaped Data:")\n'
                   'print(df_long)\n'
                   '# data.table equivalent for fast aggregation\n'
                   'dt <- as.data.table(df)\n'
                   'result <- dt[, .(mean_val1 = mean(val1)), by = group]\n'
                   'print("data.table Result:")\n'
                   'print(result)',
  'content': 'This session focuses on efficient data wrangling techniques in R using three of the most powerful '
             'packages: **dplyr**, **tidyr**, and **data.table**. Learners will explore how to clean, transform, '
             'reshape, merge, summarize, and manipulate datasets to prepare them for statistical analysis and machine '
             'learning. Emphasis is placed on writing efficient, readable, and scalable data manipulation workflows.',
  'description': 'Master advanced data wrangling and transformation using dplyr, tidyr, and data.table in R.',
  'difficulty': 'Professional',
  'duration': '60 min',
  'expected_outcomes': '* Clean messy datasets efficiently.\n'
                       '* Transform raw data into analysis-ready formats.\n'
                       '* Apply dplyr verbs such as `filter()`, `select()`, `mutate()`, `summarise()`, and '
                       '`group_by()`.\n'
                       '* Reshape data using `pivot_longer()` and `pivot_wider()`.\n'
                       '* Perform fast data processing with **data.table**.\n'
                       '* Build reproducible data wrangling workflows for real-world datasets.',
  'learning_notes': '### Data Wrangling in R\n'
                    'Data wrangling involves cleaning, reshaping, and transforming raw data into a format suitable for '
                    'analysis.\n'
                    '\n'
                    '### dplyr & tidyr\n'
                    '- pivot_longer() and pivot_wider() from tidyr reshape datasets between wide and long formats.\n'
                    '- dplyr handles group-wise transformations, filtering, and joins.\n'
                    '\n'
                    '### data.table\n'
                    'data.table is an R package that provides a high-performance version of data.frames. It is '
                    'extremely fast and memory-efficient for large datasets.',
  'notes_file_path': 'https://019f5f1f-e71d-6a8b-f340-0cf1306ef23c.share.connect.posit.cloud/',
  'objectives': '* Understand the principles of data wrangling.\n'
                '* Manipulate datasets using the **dplyr** package.\n'
                '* Reshape datasets using **tidyr**.\n'
                '* Perform high-performance data manipulation using **data.table**.\n'
                '* Merge, join, filter, group, and summarize datasets.\n'
                '* Handle missing values and duplicate records efficiently.\n'
                '* Prepare clean datasets for visualization and machine learning.',
  'quiz': [],
  'resources': '- [Tidyverse homepage](https://www.tidyverse.org/)\n'
               '- [data.table documentation](https://rdatatable.gitlab.io/data.table/)',
  'slug': 'r-session-10',
  'title': 'Session 10: Data Wrangling with dplyr, tidyr & data.table'},
 {'code_examples': 'library(ggplot2)\n'
                   '# Advanced ggplot2 customization\n'
                   'df <- data.frame(\n'
                   '  category = factor(c("A", "B", "C", "D")),\n'
                   '  value = c(23, 45, 12, 38)\n'
                   ')\n'
                   'p <- ggplot(df, aes(x = category, y = value, fill = category)) +\n'
                   '  geom_col(show.legend = FALSE) +\n'
                   '  theme_minimal(base_size = 14) +\n'
                   '  scale_fill_brewer(palette = "Set2") +\n'
                   '  labs(title = "Custom Styled Column Chart", x = "Category", y = "Value")\n'
                   'print(p)',
  'content': 'This session introduces advanced data visualization techniques using **ggplot2**, enabling learners to '
             'create professional, publication-quality visualizations. Students will learn how to customize plots, '
             'apply themes, visualize multivariate data, and communicate insights effectively through compelling '
             'graphics.',
  'description': 'Create publication-quality plots and custom visualizations using advanced ggplot2 features, plotly, '
                 'and patchworks.',
  'difficulty': 'Professional',
  'duration': '60 min',
  'expected_outcomes': '* Design professional-quality charts and graphs.\n'
                       '* Customize colors, labels, legends, and themes.\n'
                       '* Create boxplots, violin plots, heatmaps, histograms, scatterplots, and faceted '
                       'visualizations.\n'
                       '* Present analytical findings effectively.\n'
                       '* Develop dashboards and reports with meaningful visualizations.',
  'learning_notes': '### Advanced Data Visualization in R\n'
                    'Advanced data visualization involves creating customized and interactive plots that communicate '
                    'complex data insights effectively.\n'
                    '\n'
                    '### ggplot2 Themes and Customization\n'
                    '- Use theme() to customize background, grid lines, text size, and colors.\n'
                    '- Customize color and fill scales using scale_fill_brewer() or scale_color_viridis_d().\n'
                    '\n'
                    '### Plot Layouts\n'
                    'Combine multiple plots in a single figure using packages like patchwork or cowplot.',
  'notes_file_path': 'https://019f5f33-6dd3-0544-d5dd-7558d1a45bf1.share.connect.posit.cloud/',
  'objectives': '* Build advanced visualizations using **ggplot2**.\n'
                '* Customize plot aesthetics and themes.\n'
                '* Create statistical graphics for data exploration.\n'
                '* Visualize relationships among multiple variables.\n'
                '* Produce interactive and presentation-ready charts.\n'
                '* Select appropriate visualizations for different data types.',
  'quiz': [],
  'resources': '- [ggplot2 Elegant Graphics for Data Analysis](https://ggplot2-book.org/)\n'
               '- [R Graph Gallery](https://r-graph-gallery.com/)',
  'slug': 'r-session-11',
  'title': 'Session 11: Advanced Data Visualization in R'},
 {'code_examples': '# Split data and evaluate a simple baseline model\n'
                   'set.seed(42)\n'
                   'data(mtcars)\n'
                   'train_idx <- sample(1:nrow(mtcars), 0.7 * nrow(mtcars))\n'
                   'train_data <- mtcars[train_idx, ]\n'
                   'test_data <- mtcars[-train_idx, ]\n'
                   'print(paste("Train size:", nrow(train_data), "Test size:", nrow(test_data)))',
  'content': 'This session introduces statistical computing concepts and the fundamentals of machine learning using R. '
             'Learners explore descriptive and inferential statistics, probability distributions, feature engineering, '
             'model evaluation, and the overall machine learning workflow.',
  'description': 'Learn the core concepts of statistical computing, optimization, and the machine learning workflow in '
                 'R.',
  'difficulty': 'Professional',
  'duration': '60 min',
  'expected_outcomes': '* Perform statistical analysis in R.\n'
                       '* Prepare datasets for predictive modeling.\n'
                       '* Understand the machine learning lifecycle.\n'
                       '* Select suitable algorithms for different problems.\n'
                       '* Interpret model evaluation metrics.\n'
                       '* Build a strong foundation for advanced machine learning.',
  'learning_notes': '### Machine Learning Workflow\n'
                    'Machine learning is a subset of AI that enables systems to learn from data. The standard ML '
                    'workflow includes:\n'
                    '1. Data Preprocessing & Cleaning\n'
                    '2. Feature Selection & Engineering\n'
                    '3. Train/Test Splitting\n'
                    '4. Model Training & Tuning\n'
                    '5. Model Evaluation\n'
                    '\n'
                    '### Preprocessing in R\n'
                    'Use scale() to normalize numeric columns so they have a mean of 0 and standard deviation of 1.',
  'notes_file_path': 'https://019f5f3c-d9a9-9e03-83cf-2daad22a5978.share.connect.posit.cloud/',
  'objectives': '* Apply statistical techniques in R.\n'
                '* Understand supervised and unsupervised learning concepts.\n'
                '* Prepare datasets for machine learning.\n'
                '* Perform feature engineering and data preprocessing.\n'
                '* Split datasets into training and testing sets.\n'
                '* Evaluate machine learning models using appropriate metrics.',
  'quiz': [],
  'resources': '- [Introduction to Modern Statistics](https://openintro-ims.netlify.app/)\n'
               '- [Hands-On Machine Learning with R](https://bradleyboehmke.github.io/HOML/)',
  'slug': 'r-session-12',
  'title': 'Session 12: Statistical Computing & Introduction to Machine Learning'},
 {'code_examples': '# Logistic regression classification on mtcars (predicting high vs low mpg)\n'
                   'df <- mtcars\n'
                   'df$high_mpg <- as.factor(ifelse(df$mpg > 20, 1, 0))\n'
                   'model <- glm(high_mpg ~ wt + hp, data = df, family = binomial)\n'
                   'summary(model)',
  'content': 'This session introduces classification techniques used in supervised machine learning. Learners will '
             'build models capable of predicting categorical outcomes using algorithms such as Logistic Regression, '
             'Decision Trees, Random Forest, Naïve Bayes, K-Nearest Neighbors (KNN), and Support Vector Machines '
             '(SVM).',
  'description': 'Train, evaluate, and tune classification models in R using caret and tidymodels.',
  'difficulty': 'Professional',
  'duration': '75 min',
  'expected_outcomes': '* Develop classification models for real-world datasets.\n'
                       '* Predict categorical outcomes accurately.\n'
                       '* Evaluate model performance using Accuracy, Precision, Recall, F1-Score, and ROC-AUC.\n'
                       '* Improve model performance through parameter tuning.\n'
                       '* Select appropriate classification techniques for different business problems.',
  'learning_notes': '### Supervised Classification\n'
                    'Classification is a type of supervised learning where the target variable is categorical (e.g. '
                    'Pass/Fail, Yes/No).\n'
                    '\n'
                    '### Logistic Regression\n'
                    'Used when predicting a binary outcome. It models the log-odds of the probability of class 1.\n'
                    '\n'
                    '### Decision Trees & Random Forests\n'
                    'Decision trees split data recursively based on feature thresholds. Random Forests combine '
                    'multiple trees for better generalizability.',
  'notes_file_path': 'https://019f5f3a-de8f-352f-c0c4-f987772281b3.share.connect.posit.cloud/',
  'objectives': '* Understand classification problems.\n'
                '* Build classification models in R.\n'
                '* Train and test classification algorithms.\n'
                '* Evaluate classification performance.\n'
                '* Interpret confusion matrices and classification metrics.\n'
                '* Compare multiple classification algorithms.',
  'quiz': [],
  'resources': '- [Tidymodels documentation](https://www.tidymodels.org/)\n'
               '- [Caret package manual](https://topepo.github.io/caret/)',
  'slug': 'r-session-13',
  'title': 'Session 13: Supervised Machine Learning | Classification'},
 {'code_examples': '# Multiple linear regression in R\nmodel <- lm(mpg ~ wt + hp + cyl, data = mtcars)\nsummary(model)',
  'content': 'This session explores regression techniques for predicting continuous numerical outcomes. Learners build '
             'and evaluate regression models using Linear Regression, Multiple Regression, Polynomial Regression, and '
             'Regularization techniques to solve predictive analytics problems.',
  'description': 'Train, tune, and evaluate regression models in R to predict continuous variables.',
  'difficulty': 'Professional',
  'duration': '75 min',
  'expected_outcomes': '* Develop predictive regression models.\n'
                       '* Analyze relationships between variables.\n'
                       '* Evaluate models using RMSE, MAE, and R².\n'
                       '* Interpret regression outputs confidently.\n'
                       '* Apply regression techniques to business and research datasets.',
  'learning_notes': '### Supervised Regression\n'
                    'Regression is used to predict continuous outcomes (e.g., house prices, sales, yields).\n'
                    '\n'
                    '### Regularization\n'
                    '- **Lasso Regression (L1)**: Adds a penalty equivalent to the absolute values of the '
                    'coefficients, pushing some to zero (feature selection).\n'
                    '- **Ridge Regression (L2)**: Adds a penalty equivalent to the square of the coefficients, '
                    'shrinking them towards zero.\n'
                    '\n'
                    '### Evaluation Metrics\n'
                    '- Root Mean Squared Error (RMSE): Average magnitude of error.\n'
                    '- R-squared: Proportion of variance explained by model.',
  'notes_file_path': 'https://019f5f53-62bf-c5b5-e834-ed3252d834f3.share.connect.posit.cloud/',
  'objectives': '* Understand regression analysis concepts.\n'
                '* Build regression models in R.\n'
                '* Interpret regression coefficients.\n'
                '* Evaluate regression performance.\n'
                '* Detect overfitting and underfitting.\n'
                '* Improve predictive accuracy.',
  'quiz': [],
  'resources': '- [An Introduction to Statistical Learning](https://www.statlearning.com/)\n'
               '- [Tidymodels for Regression](https://www.tidymodels.org/start/models/)',
  'slug': 'r-session-14',
  'title': 'Session 14: Supervised Machine Learning | Regression'},
 {'code_examples': '# K-means clustering on mtcars numeric columns\n'
                   'numeric_data <- scale(mtcars[, c("mpg", "disp", "hp", "wt")])\n'
                   'set.seed(42)\n'
                   'clusters <- kmeans(numeric_data, centers = 3)\n'
                   'print(clusters$centers)',
  'content': 'This session introduces unsupervised learning techniques that identify hidden structures within '
             'datasets. Learners will perform clustering and dimensionality reduction using algorithms such as '
             'K-Means, Hierarchical Clustering, Principal Component Analysis (PCA), and t-SNE to discover patterns '
             'without predefined labels.',
  'description': 'Discover hidden structures in unlabeled datasets using clustering and dimensionality reduction in R.',
  'difficulty': 'Professional',
  'duration': '75 min',
  'expected_outcomes': '* Segment data into meaningful groups.\n'
                       '* Apply K-Means and Hierarchical Clustering.\n'
                       '* Reduce dataset dimensions using PCA.\n'
                       '* Visualize complex datasets effectively.\n'
                       '* Extract meaningful insights from unlabeled data.',
  'learning_notes': '### Unsupervised Learning\n'
                    'Unsupervised learning works with unlabeled datasets. Its goals include clustering and dimension '
                    'reduction.\n'
                    '\n'
                    '### Clustering\n'
                    '- **K-Means**: Groups observations based on their distance to a central centroid.\n'
                    '- **Hierarchical Clustering**: Builds a tree of clusters (dendrogram) based on pairwise '
                    'distances.\n'
                    '\n'
                    '### Dimension Reduction (PCA)\n'
                    'PCA converts a set of correlated variables into a set of values of linearly uncorrelated '
                    'variables called principal components.',
  'notes_file_path': 'https://019f5f57-7e38-8f53-3e0b-b31b94057808.share.connect.posit.cloud/',
  'objectives': '* Understand unsupervised learning concepts.\n'
                '* Perform clustering analysis.\n'
                '* Apply dimensionality reduction techniques.\n'
                '* Visualize high-dimensional datasets.\n'
                '* Interpret clusters and hidden patterns.\n'
                '* Evaluate clustering performance.',
  'quiz': [],
  'resources': '- [Unsupervised Learning on CRAN](https://cran.r-project.org/web/views/Cluster.html)\n'
               '- [PCA in R Tutorial](https://www.r-bloggers.com/2021/05/principal-component-analysis-pca-in-r/)',
  'slug': 'r-session-15',
  'title': 'Session 15: Unsupervised Machine Learning | Clustering & Dimension Reduction'},
 {'code_examples': '# Capstone end-to-end simulation\nprint("CDAM R Capstone Project Pipeline Initialized")',
  'content': 'The final session provides learners with the opportunity to apply all the knowledge and skills acquired '
             'throughout the course by completing comprehensive real-world data science projects using R. Students '
             'will independently plan, implement, analyze, visualize, and present end-to-end analytical solutions '
             'while demonstrating proficiency in data wrangling, statistical analysis, visualization, and machine '
             'learning.',
  'description': 'Apply your machine learning and statistical computing skills to solve a comprehensive real-world '
                 'problem in R.',
  'difficulty': 'Professional',
  'duration': '120 min',
  'expected_outcomes': '* Develop complete end-to-end data science solutions in R.\n'
                       '* Apply industry-standard analytical workflows.\n'
                       '* Build professional portfolios showcasing practical projects.\n'
                       '* Demonstrate readiness for real-world data analytics roles.\n'
                       '* Present data-driven insights confidently to technical and non-technical audiences.',
  'learning_notes': '### R Capstone Project\n'
                    'The capstone is an integration of all key R capabilities. It represents the final step in the '
                    'Professional R Track, allowing you to showcase an end-to-end statistical modeling or machine '
                    'learning solution.',
  'notes_file_path': 'https://019f5f78-17b4-f53f-98ee-ab41aa5595c0.share.connect.posit.cloud/',
  'objectives': '* Integrate all concepts learned throughout the course.\n'
                '* Design and execute complete data science projects.\n'
                '* Perform data cleaning, analysis, visualization, and modeling.\n'
                '* Document analytical workflows professionally.\n'
                '* Communicate analytical findings effectively.\n'
                '* Present project results using reproducible reports.',
  'quiz': [],
  'resources': '- [CDAM R Graduation Requirements](https://cdam.chuka.ac.ke/grad/r/)\n'
               '- [R Markdown Guide](https://bookdown.org/yihui/rmarkdown/)',
  'slug': 'r-session-16',
  'title': 'Session 16: Capstone Projects in R'}]
