"""Course seed data for CDAM Python for Data Science Masterclass."""

SESSIONS = [
    {
        "title": "Introduction to Python",
        "slug": "introduction-to-python",
        "description": "Get started with Python syntax, tooling, and workflow for data science.",
        "duration": "45 min",
        "difficulty": "Beginner",
        "objectives": """- Understand Python's role in data science and AI
- Set up a productive coding environment
- Run scripts and Jupyter notebooks
- Use variables, comments, and basic syntax""",
        "content": """## Welcome to Python for Data Science

Python is the most widely used language in analytics, machine learning, and AI. At **CDAM** (Center for Data Analytics & Modelling), we use Python to turn raw data into actionable insights.

### Why Python?

- Readable syntax that mirrors plain English
- Rich ecosystem: NumPy, Pandas, Matplotlib, scikit-learn
- Strong community and industry adoption

### Your First Steps

1. Install Python 3.10+
2. Create a virtual environment
3. Launch Jupyter Lab or VS Code
4. Run your first script

> **CDAM Tip:** Practice daily — even 20 minutes builds momentum.""",
        "code_examples": """# Your first Python program
print('Hello, CDAM Data Science!')

# Basic arithmetic for analytics
total_sales = 1200 + 850 + 430
average = total_sales / 3
print(f'Average sales: {average:.2f}')""",
        "resources": """- [Python Official Docs](https://docs.python.org/3/)
- [Jupyter Project](https://jupyter.org/)
- [CDAM Training Portal](https://cdam.chuka.ac.ke/training/)""",
        "quiz": [
            {"question": "What makes Python popular in data science?", "options": ["Readable syntax and rich libraries", "It only runs on Windows", "No community support", "Cannot integrate with databases"], "correct": 0},
            {"question": "Which tool is commonly used for interactive notebooks?", "options": ["Jupyter", "Photoshop", "Excel only", "Notepad"], "correct": 0},
            {"question": "What does print() do?", "options": ["Outputs text to the console", "Deletes files", "Installs packages", "Creates a database"], "correct": 0},
        ],
    },
    {
        "title": "Variables and Data Types",
        "slug": "variables-and-data-types",
        "description": "Learn primitives, collections, and data conversions.",
        "duration": "50 min",
        "difficulty": "Beginner",
        "objectives": """- Use integers, floats, strings, and booleans
- Work with lists, tuples, and dictionaries
- Cast between types safely
- Inspect values with type()""",
        "content": """## Variables and Data Types

Variables are named containers for data. Python is **dynamically typed** — you don't declare types explicitly.

### Core Types

| Type | Example | Use Case |
|------|---------|----------|
| int | `42` | Counts, IDs |
| float | `3.14` | Measurements |
| str | `'CDAM'` | Text labels |
| bool | `True` | Flags, conditions |
| list | `[1, 2, 3]` | Ordered collections |
| dict | `{'a': 1}` | Key-value records |""",
        "code_examples": """name = 'CDAM Scholar'
age = 25
height = 5.9
is_enrolled = True

scores = [88, 92, 79]
student = {'name': name, 'scores': scores}

print(type(name), type(scores), type(student))""",
        "resources": """- [Python Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- [Real Python: Data Types](https://realpython.com/python-data-types/)""",
        "quiz": [
            {"question": "Which type stores key-value pairs?", "options": ["dict", "int", "float", "bool"], "correct": 0},
            {"question": "What is the output type of 5 / 2 in Python 3?", "options": ["float", "int", "str", "list"], "correct": 0},
            {"question": "Which collection is ordered and mutable?", "options": ["list", "tuple", "int", "None"], "correct": 0},
        ],
    },
    {
        "title": "Control Flow and Functions",
        "slug": "control-flow-and-functions",
        "description": "Use conditionals, loops, and reusable functions.",
        "duration": "60 min",
        "difficulty": "Beginner",
        "objectives": """- Write if/elif/else branching logic
- Iterate with for and while loops
- Build reusable functions with parameters
- Return values from functions""",
        "content": """## Control Flow and Functions

Control flow lets your programs make decisions and repeat tasks — essential for data pipelines.

### Conditionals

Use `if`, `elif`, and `else` to branch based on data quality checks, thresholds, or categories.

### Loops

- **for** — iterate over lists, DataFrame rows, file lines
- **while** — repeat until a condition is met

### Functions

Encapsulate logic for reuse, testing, and cleaner notebooks.""",
        "code_examples": """def grade(score):
    if score >= 70:
        return 'Pass'
    elif score >= 50:
        return 'Retake'
    return 'Fail'

results = []
for score in [45, 67, 82, 91]:
    results.append(grade(score))
print(results)""",
        "resources": """- [Python Control Flow](https://docs.python.org/3/tutorial/controlflow.html)
- [Functions in Python](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)""",
        "quiz": [
            {"question": "Which keyword defines a function?", "options": ["def", "func", "function", "lambda only"], "correct": 0},
            {"question": "What loop iterates over a sequence?", "options": ["for", "if", "import", "class"], "correct": 0},
            {"question": "elif stands for?", "options": ["else if", "every loop", "error log", "element index"], "correct": 0},
        ],
    },
    {
        "title": "NumPy Fundamentals",
        "slug": "numpy-fundamentals",
        "description": "Work with high-performance arrays and vectorized operations.",
        "duration": "70 min",
        "difficulty": "Intermediate",
        "objectives": """- Create and reshape ndarrays
- Apply vectorized math operations
- Understand broadcasting and indexing
- Compute summary statistics on arrays""",
        "content": """## NumPy Fundamentals

NumPy provides **ndarrays** — fast, homogeneous arrays that power Pandas and scikit-learn.

### Key Concepts

- **Vectorization** — apply operations to entire arrays without Python loops
- **Broadcasting** — align differently shaped arrays for computation
- **Indexing** — slice and filter like a pro

NumPy is typically 10–100x faster than pure Python lists for numerical work.""",
        "code_examples": """import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print('Mean:', arr.mean())
print('Doubled:', arr * 2)

matrix = np.array([[1, 2], [3, 4]])
print('Shape:', matrix.shape)
print('Sum axis 0:', matrix.sum(axis=0))""",
        "resources": """- [NumPy Documentation](https://numpy.org/doc/)
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)""",
        "quiz": [
            {"question": "What is NumPy's core data structure?", "options": ["ndarray", "DataFrame", "Series", "Graph"], "correct": 0},
            {"question": "Vectorization helps by?", "options": ["Avoiding slow Python loops", "Deleting data", "Creating HTML", "Sending emails"], "correct": 0},
            {"question": "arr.mean() returns?", "options": ["Average of array elements", "Maximum value", "Array length", "Random number"], "correct": 0},
        ],
    },
    {
        "title": "Pandas Data Analysis",
        "slug": "pandas-data-analysis",
        "description": "Analyze tabular data using DataFrames and Series.",
        "duration": "75 min",
        "difficulty": "Intermediate",
        "objectives": """- Load CSV and Excel files into DataFrames
- Inspect data with head(), info(), describe()
- Filter rows and select columns
- Group and aggregate data""",
        "content": """## Pandas Data Analysis

Pandas is the workhorse of tabular data analysis in Python.

### DataFrame Essentials

- **Series** — single column with an index
- **DataFrame** — table of Series sharing an index
- **read_csv()** — load data from files

Analysts spend most of their time exploring, filtering, and summarizing DataFrames.""",
        "code_examples": """import pandas as pd

df = pd.DataFrame({
    'student': ['Alice', 'Bob', 'Carol'],
    'score': [88, 72, 95],
    'course': ['Python', 'Python', 'ML']
})

print(df.describe())
print(df[df['score'] >= 80])""",
        "resources": """- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)""",
        "quiz": [
            {"question": "Which function loads CSV files?", "options": ["read_csv", "load_csv", "open_csv", "import_csv"], "correct": 0},
            {"question": "df.describe() shows?", "options": ["Summary statistics", "Only column names", "File path", "Plot colors"], "correct": 0},
            {"question": "A single column in Pandas is called?", "options": ["Series", "Matrix", "Tensor", "Node"], "correct": 0},
        ],
    },
    {
        "title": "Data Cleaning and Manipulation",
        "slug": "data-cleaning-and-manipulation",
        "description": "Handle missing values, duplicates, and inconsistent formats.",
        "duration": "70 min",
        "difficulty": "Intermediate",
        "objectives": """- Detect missing and duplicate records
- Impute or drop null values strategically
- Standardize text and date formats
- Validate cleaned datasets""",
        "content": """## Data Cleaning and Manipulation

Real-world data is messy. Cleaning typically consumes **60–80%** of an analyst's time.

### Common Issues

- Missing values (NaN, null, blank strings)
- Duplicate rows
- Inconsistent categories (`'Male'`, `'M'`, `'male'`)
- Wrong data types

Clean data → reliable models → trustworthy decisions.""",
        "code_examples": """import pandas as pd
import numpy as np

df = pd.DataFrame({'age': [22, np.nan, 30, 22], 'city': ['Nairobi', 'Nairobi', None, 'Nairobi']})
df = df.drop_duplicates()
df['age'] = df['age'].fillna(df['age'].median())
df['city'] = df['city'].fillna('Unknown')
print(df)""",
        "resources": """- [Handling Missing Data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [CDAM Research Projects](https://cdam.chuka.ac.ke/projects/)""",
        "quiz": [
            {"question": "fillna() is used to?", "options": ["Replace missing values", "Delete all rows", "Create plots", "Export PDF"], "correct": 0},
            {"question": "drop_duplicates() removes?", "options": ["Repeated rows", "Column headers", "File names", "Indexes only"], "correct": 0},
            {"question": "Why clean data before modeling?", "options": ["Improves model reliability", "Slows analysis", "Is optional always", "Removes all features"], "correct": 0},
        ],
    },
    {
        "title": "Data Visualization with Matplotlib and Seaborn",
        "slug": "data-visualization-matplotlib-seaborn",
        "description": "Create plots that communicate trends and comparisons clearly.",
        "duration": "80 min",
        "difficulty": "Intermediate",
        "objectives": """- Build line, bar, scatter, and histogram charts
- Customize titles, labels, and legends
- Apply Seaborn themes and color palettes
- Choose the right chart for your data story""",
        "content": """## Data Visualization

Great visualizations turn numbers into narratives. Use **Matplotlib** for fine control and **Seaborn** for statistical plots with less code.

### Chart Selection Guide

- **Trend over time** → line chart
- **Category comparison** → bar chart
- **Relationship** → scatter plot
- **Distribution** → histogram / KDE""",
        "code_examples": """import matplotlib.pyplot as plt
import seaborn as sns

tips = sns.load_dataset('tips')
sns.set_theme(style='darkgrid')
sns.histplot(data=tips, x='total_bill', kde=True)
plt.title('Restaurant Bill Distribution')
plt.show()""",
        "resources": """- [Matplotlib Docs](https://matplotlib.org/stable/contents.html)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)""",
        "quiz": [
            {"question": "Which library adds statistical plot styles on Matplotlib?", "options": ["Seaborn", "Requests", "Flask", "SQLite"], "correct": 0},
            {"question": "A histogram shows?", "options": ["Distribution of values", "Network connections", "SQL queries", "File sizes only"], "correct": 0},
            {"question": "plt.title() sets?", "options": ["Chart title", "X-axis label", "Color palette", "Database name"], "correct": 0},
        ],
    },
    {
        "title": "Statistical Analysis",
        "slug": "statistical-analysis",
        "description": "Apply descriptive and inferential statistics to data.",
        "duration": "65 min",
        "difficulty": "Intermediate",
        "objectives": """- Compute mean, median, variance, and standard deviation
- Understand probability distributions
- Formulate and test hypotheses
- Interpret p-values responsibly""",
        "content": """## Statistical Analysis for Data Science

Statistics helps you quantify uncertainty and test whether patterns are real or random.

### Descriptive vs Inferential

- **Descriptive** — summarize what happened (mean, median, SD)
- **Inferential** — infer about populations from samples (t-tests, chi-square)

Always pair statistical tests with domain knowledge.""",
        "code_examples": """import numpy as np
from scipy import stats

data = np.array([12, 15, 14, 18, 11, 16, 13])
print('Mean:', np.mean(data))
print('Median:', np.median(data))
print('Std Dev:', np.std(data, ddof=1))

t_stat, p_value = stats.ttest_1samp(data, popmean=15)
print(f'p-value: {p_value:.4f}')""",
        "resources": """- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [CDAM Research](https://cdam.chuka.ac.ke/research/)""",
        "quiz": [
            {"question": "Standard deviation measures?", "options": ["Spread of data", "Sum of values", "Row count", "File size"], "correct": 0},
            {"question": "A p-value helps assess?", "options": ["Statistical significance", "Plot colors", "Memory usage", "Network speed"], "correct": 0},
            {"question": "Median is resistant to?", "options": ["Outliers", "All missing data", "Column names", "CSV headers"], "correct": 0},
        ],
    },
    {
        "title": "Machine Learning Basics with Scikit-learn",
        "slug": "machine-learning-basics-scikit-learn",
        "description": "Train and evaluate baseline ML models.",
        "duration": "90 min",
        "difficulty": "Intermediate",
        "objectives": """- Split data into train and test sets
- Train classification and regression models
- Evaluate with accuracy, precision, recall, RMSE
- Understand overfitting basics""",
        "content": """## Machine Learning Basics

scikit-learn provides consistent APIs for classical ML algorithms — ideal for baselines before deep learning.

### ML Workflow

1. Prepare features and target
2. Split train/test
3. Train a model
4. Evaluate metrics
5. Iterate and improve

Start simple: logistic regression or random forests often perform surprisingly well.""",
        "code_examples": """from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)
print('Accuracy:', accuracy_score(y_test, preds))""",
        "resources": """- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Model Selection](https://scikit-learn.org/stable/model_selection.html)""",
        "quiz": [
            {"question": "train_test_split prevents?", "options": ["Testing on training data only", "Using Python", "Reading CSV", "Plotting charts"], "correct": 0},
            {"question": "RandomForestClassifier is for?", "options": ["Classification", "SQL queries", "Web scraping", "Image compression"], "correct": 0},
            {"question": "accuracy_score compares?", "options": ["Predictions vs true labels", "Two CSV files", "Plot sizes", "Memory usage"], "correct": 0},
        ],
    },
    {
        "title": "Time Series Analysis",
        "slug": "time-series-analysis",
        "description": "Work with temporal data and basic forecasting workflows.",
        "duration": "95 min",
        "difficulty": "Advanced",
        "objectives": """- Parse and index datetime columns
- Resample and roll time-based aggregations
- Identify trend and seasonality
- Build simple forecasting baselines""",
        "content": """## Time Series Analysis

Time series data appears everywhere: sales, weather, health metrics, malaria cases — a core focus at CDAM.

### Key Techniques

- **Datetime indexing** — sort and slice by date
- **Resampling** — daily → weekly/monthly aggregates
- **Rolling windows** — moving averages
- **Forecasting** — predict future values from history

Always visualize your series before modeling.""",
        "code_examples": """import pandas as pd

dates = pd.date_range('2024-01-01', periods=6, freq='M')
sales = [120, 135, 128, 150, 160, 172]
df = pd.DataFrame({'sales': sales}, index=dates)
df.index.name = 'date'

monthly_avg = df.resample('M').mean()
rolling = df['sales'].rolling(window=3).mean()
print(rolling.tail())""",
        "resources": """- [Pandas Time Series](https://pandas.pydata.org/docs/user_guide/timeseries.html)
- [CDAM Malaria AI Projects](https://cdam.chuka.ac.ke/projects/)""",
        "quiz": [
            {"question": "pd.to_datetime converts?", "options": ["Strings to datetime objects", "Images to arrays", "HTML to PDF", "SQL to JSON"], "correct": 0},
            {"question": "Rolling window computes?", "options": ["Moving aggregates", "Random samples", "Duplicate rows", "File checksums"], "correct": 0},
            {"question": "Time series index is usually?", "options": ["Datetime ordered", "Alphabetical", "Random", "Binary"], "correct": 0},
        ],
    },
]
