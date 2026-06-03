"""Course seed data for CDAM Python for Data Science Masterclass with rich interactive details."""

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
        "expected_outcomes": """### Knowledge Outcomes
- Understand Python's design philosophy (readability and simplicity) and its role in Data Science, Machine Learning, and AI.
- Explain the difference between Python scripts (.py) and interactive notebooks (.ipynb).
- Understand Python variables, data types, and basic arithmetic syntax.

### Practical Outcomes
- Install and verify a Python 3.10+ environment.
- Execute basic Python commands in a terminal or Jupyter environment.
- Write clean code using proper indentation, variables, and formatting.

### Industry-Relevant Skills
- Setting up professional development environments (VS Code, Jupyter, Virtual Environments) for project reproducibility.
""",
        "learning_notes": """### Concept Explanation & Theory
Python is an interpreted, high-level, general-purpose programming language. Created by Guido van Rossum and released in 1991, Python's design philosophy emphasizes code readability through its notable use of significant whitespace. Today, it is the standard for Data Science, Machine Learning, and Artificial Intelligence due to its rich ecosystem of libraries.

### Important Definitions
- **Variable:** A named location in memory used to store data.
- **Syntax:** The set of rules defining how a program is written and interpreted.
- **Sandbox:** A secure environment to execute code without affecting local resources.

### Best Practices
- Follow PEP 8 style guidelines (e.g., use 4 spaces per indentation level).
- Use descriptive variable names (e.g., `total_sales` instead of `x`).

### Common Mistakes
- Mixing tabs and spaces, which causes `IndentationError` in Python.
- Using Python keywords (e.g., `print`, `if`, `class`) as variable names.

### Tips & Warnings
> 💡 **Tip:** Always document your code using comments (`#`) so others (and your future self) understand the logic.
""",
        "instructions": """#### What you will do:
In this simulation, you will run a simple Python script that outputs text and computes average sales.

#### Step-by-Step Instructions:
1. **Step 1:** Run the default code by clicking the **Run Code** button. Observe the output printed in the console.
2. **Step 2:** Modify the variable values: change `total_sales = 1200 + 850 + 430` to reflect new sales figures, e.g., `total_sales = 1500 + 950 + 550`.
3. **Step 3:** Click **Run Code** again to see the updated average sales calculation.
""",
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
        "expected_outcomes": """### Knowledge Outcomes
- Explain dynamic typing and how variables hold references in memory.
- Identify the differences between primitive types (int, float, str, bool) and collections (list, dict, tuple, set).
- Understand readability advantages of explicit type casting.

### Practical Outcomes
- Declare variables of various data types.
- Perform list modifications (appending, slicing) and dictionary lookups.
- Print type information using the `type()` built-in function.

### Industry-Relevant Skills
- Structuring raw, multi-format datasets into Python primitive collections for quick local analysis.
""",
        "learning_notes": """### Concept Explanation & Theory
Variables in Python are pointers to memory addresses where data objects reside. Since Python is dynamically typed, the interpreter infers the data type based on the value assigned, allowing high developer flexibility.

### Important Definitions
- **int / float:** Primitives for whole numbers and decimal fractions.
- **list:** An ordered, mutable sequence of items.
- **dict:** A mapping of keys to values (like a JSON object).

### Best Practices
- Keep variable names descriptive and lowercase (snake_case).
- Keep lists homogeneous where possible, and use dictionaries for structured records.

### Common Mistakes
- Trying to concatenate strings and numbers without casting: `print("Age: " + age)`. Use f-strings instead: `print(f"Age: {age}")`.
- Modifying a list while iterating over it.

### Tips & Warnings
> 💡 **Tip:** Use `type(variable_name)` to debug type mismatches.
""",
        "instructions": """#### What you will do:
In this simulation, you will declare variables, use primitive lists and dictionaries, and output their type information.

#### Step-by-Step Instructions:
1. **Step 1:** Click **Run Code** and review the types printed.
2. **Step 2:** Add a new key-value pair to the `student` dictionary, e.g., `student['gpa'] = 3.8`.
3. **Step 3:** Append a new score to the `scores` list: `scores.append(95)`.
4. **Step 4:** Run the code and verify the updated output.
""",
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
        "expected_outcomes": """### Knowledge Outcomes
- Explain logical branching and truthiness in conditional evaluation.
- Understand the differences between fixed iterations (`for`) and conditional loops (`while`).
- Comprehend lexical scoping and function return mechanics.

### Practical Outcomes
- Write complex `if-elif-else` structures.
- Traverse sequences using `for` loops.
- Define, document, and test modular functions with parameters.

### Industry-Relevant Skills
- Automating business logic and decision pipelines in data validation workflows.
""",
        "learning_notes": """### Concept Explanation & Theory
Control flow commands direct the execution path of a program. Functions allow developers to write modular, reusable blocks of logic, reducing redundancy (DRY: Don't Repeat Yourself).

### Important Definitions
- **Boolean Expression:** An statement evaluating to `True` or `False`.
- **Iteration:** Repeating a block of instructions a specified number of times or while a condition is met.
- **Scope:** The region of a program where a variable is accessible.

### Best Practices
- Keep functions small and focused on a single task (Single Responsibility).
- Always include return statements explicitly when returning results.

### Common Mistakes
- Forgetting the colon `:` at the end of function definitions, loops, or conditionals.
- Infinite loops when writing `while` loops due to missing update conditions.

### Tips & Warnings
> 💡 **Tip:** Use descriptive verbs to name functions (e.g., `calculate_mean` instead of `calc`).
""",
        "instructions": """#### What you will do:
You will modify and test a grading function that loops through scores.

#### Step-by-Step Instructions:
1. **Step 1:** Run the script. Examine the passed/failed results.
2. **Step 2:** Modify the logic of the `grade` function. For example, add a distinction grade: `if score >= 90: return 'Distinction'`.
3. **Step 3:** Change the input scores list to include `95` and `35`.
4. **Step 4:** Run again to observe the updated lists of grades.
""",
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
        "expected_outcomes": """### Knowledge Outcomes
- Explain why NumPy arrays are faster and consume less memory than Python lists.
- Describe the concepts of vectorization and broadcasting.
- Understand dimensional representations (axes) in multi-dimensional arrays.

### Practical Outcomes
- Initialize arrays using `np.array()`, `np.zeros()`, `np.ones()`, and `np.arange()`.
- Reshape, slice, and filter arrays using boolean indexing.
- Compute mathematical metrics (mean, median, standard deviation) across specific axes.

### Industry-Relevant Skills
- Efficient numerical computations on matrices representing image data, scientific experiments, or financial portfolios.
""",
        "learning_notes": """### Concept Explanation & Theory
NumPy (Numerical Python) is the foundation of scientific computing in Python. It provides high-performance multi-dimensional array objects (`ndarrays`) which are compiled in C, allowing fast contiguous memory access and vectorized math operations.

### Important Definitions
- **Vectorization:** Performing batch operations on data without writing slow, manual loops.
- **Broadcasting:** How NumPy treats arrays of different shapes during arithmetic operations.
- **Axis:** Dimensions of an array. Axis 0 represents columns/vertical, and Axis 1 represents rows/horizontal.

### Best Practices
- Never use python loops (`for`, `while`) to perform arithmetic over NumPy arrays; utilize vectorized methods.
- Specify axes explicitly in operations like `.sum()` and `.mean()`.

### Common Mistakes
- Confusing array shapes when multiplying matrices (e.g., trying to dot multiply mismatched dimensions).

### Tips & Warnings
> 💡 **Tip:** Slicing a NumPy array returns a *view*, not a copy. Changing the slice modifies the original array!
""",
        "instructions": """#### What you will do:
You will experiment with array creation, element-wise math, and array axes.

#### Step-by-Step Instructions:
1. **Step 1:** Run the starter code. Note the axis 0 sum and mean values.
2. **Step 2:** Modify the `arr` array to have different numbers.
3. **Step 3:** Calculate and print the standard deviation of `arr` using `arr.std()`.
4. **Step 4:** Run again to check the calculated values.
""",
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
        "expected_outcomes": """### Knowledge Outcomes
- Differentiate between a Pandas Series and a DataFrame.
- Understand the role of indexing in tabular operations.
- Describe how Pandas maps to standard SQL operations (selection, joins, grouping).

### Practical Outcomes
- Create DataFrames dynamically or load them from data sources.
- Filter records using boolean conditions.
- Group rows and compute aggregate functions like mean, count, and sum.

### Industry-Relevant Skills
- Loading and summarizing business metrics (sales, active users, clinical trials) to generate immediate insights.
""",
        "learning_notes": """### Concept Explanation & Theory
Pandas is built on top of NumPy and is the industry standard tool for data manipulation and analysis. It introduces the DataFrame, which is a 2D labeled data structure with columns of potentially different types, resembling an SQL table or an Excel sheet.

### Important Definitions
- **Series:** A 1D labeled array capable of holding any data type.
- **DataFrame:** A 2D labeled, size-mutable tabular data structure.
- **Aggregation:** Summarizing multiple values into a single summary statistics figure (e.g., grouping by city and getting the mean age).

### Best Practices
- Always inspect loaded data using `df.info()` to check data types and null counts.
- Use `.loc` and `.iloc` for explicit index-based slicing.

### Common Mistakes
- Chained indexing like `df[df['A'] > 2]['B'] = 3` which can trigger a `SettingWithCopyWarning`.

### Tips & Warnings
> 💡 **Tip:** Use `df.describe()` for a quick statistical snapshot of all numeric columns in a DataFrame.
""",
        "instructions": """#### What you will do:
You will query a sample student DataFrame, filter it, and print basic statistics.

#### Step-by-Step Instructions:
1. **Step 1:** Run the script and observe the descriptive statistics table and filtered student list.
2. **Step 2:** Modify the filter condition: display only students whose score is greater than or equal to 90.
3. **Step 3:** Add a new student record for 'David' with a score of 81 in the 'ML' course.
4. **Step 4:** Run again to check the updated statistics.
""",
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
        "expected_outcomes": """### Knowledge Outcomes
- Explain why data cleaning is critical and how dirty data leads to corrupted models (Garbage In, Garbage Out).
- Evaluate when to drop vs when to impute (fill) missing values.
- Understand duplication criteria in complex tables.

### Practical Outcomes
- Detect nulls using `.isna()` or `.isnull()`.
- Impute missing values with median, mean, or static values using `.fillna()`.
- Remove duplicate rows with `.drop_duplicates()`.

### Industry-Relevant Skills
- Transforming raw, messy operational data into high-integrity training sets for predictive modeling.
""",
        "learning_notes": """### Concept Explanation & Theory
In the real world, datasets are rarely clean. They contain missing records, duplicate rows, system glitches, and bad input formats. Data cleaning is the process of detecting and correcting (or removing) corrupt or inaccurate records from a recordset.

### Important Definitions
- **Imputation:** Replacing missing data with substituted values (like mean or median).
- **Null Value:** Missing or undefined value representation (e.g., `NaN` in Pandas).
- **Duplicate:** Rows sharing identical column values, representing redundant data entry.

### Best Practices
- Never use the mean to impute when data has strong outliers; use the median.
- Document every cleaning step so data pipelines can be replicated.

### Common Mistakes
- Dropping all rows with any missing values without assessing the loss of information.

### Tips & Warnings
> 💡 **Tip:** Always verify rows before and after running `.drop_duplicates()` to know exactly how many rows were purged.
""",
        "instructions": """#### What you will do:
You will clean a small dataset containing duplicate records and null fields.

#### Step-by-Step Instructions:
1. **Step 1:** Run the script and observe the cleaned DataFrame. Note the median replacement for age.
2. **Step 2:** Modify the code to fill missing 'city' values with 'Nairobi' instead of 'Unknown'.
3. **Step 3:** Add another record to the DataFrame that has missing age and missing city, and verify how it gets cleaned.
4. **Step 4:** Run the simulator to test your logic.
""",
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
        "expected_outcomes": """### Knowledge Outcomes
- Understand the roles of Matplotlib (low-level, complete control) and Seaborn (high-level statistical wrapper).
- List the main chart types and when to apply them based on variable types (categorical vs continuous).
- Evaluate graphic integrity rules (e.g., labeling, appropriate scaling).

### Practical Outcomes
- Generate plots using `sns.histplot`, `sns.scatterplot`, and standard Matplotlib.
- Customize title labels, axes labels, legends, and styling grid layouts.
- Save and render figures.

### Industry-Relevant Skills
- Building corporate-ready data visualizations to communicate analytical findings to stakeholders.
""",
        "learning_notes": """### Concept Explanation & Theory
Visualization is key to understanding and presenting data. While tables tell part of the story, visual formats expose clusters, trends, outliers, and distributions immediately.

### Important Definitions
- **Histogram:** A plot showing the distribution of a single continuous variable.
- **Scatter Plot:** A plot showing the relationship between two continuous variables.
- **KDE (Kernel Density Estimate):** A smooth curve representing the probability density function.

### Best Practices
- Never crowd charts; use legends and clear titles.
- Choose color palettes that are accessible and professional.

### Common Mistakes
- Mislabeling axes or failing to declare units of measurement.

### Tips & Warnings
> 💡 **Tip:** Seaborn themes can be applied globally using `sns.set_theme(style='whitegrid')`.
""",
        "instructions": """#### What you will do:
You will load the sample 'tips' dataset and visualize its distributions.

#### Step-by-Step Instructions:
1. **Step 1:** Run the script. Note the histogram distribution output.
2. **Step 2:** Change the histogram target variable from `x='total_bill'` to `x='tip'`.
3. **Step 3:** Change the Seaborn style theme to `style='whitegrid'`.
4. **Step 4:** Run again to compare visual results.
""",
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
        "expected_outcomes": """### Knowledge Outcomes
- Distinguish between descriptive (summarizing samples) and inferential (generalizing to populations) statistics.
- Define null (`H0`) and alternative (`H1`) hypotheses.
- Explain what a p-value represents and how to compare it against a significance level (alpha = 0.05).

### Practical Outcomes
- Calculate basic parameters (mean, median, std) with NumPy.
- Perform a single-sample t-test using `scipy.stats`.
- Correctly accept or reject hypotheses based on the p-value.

### Industry-Relevant Skills
- Conducting A/B testing, clinical trial validations, and evaluating business experiments scientifically.
""",
        "learning_notes": """### Concept Explanation & Theory
Statistics helps data scientists extract signals from noise, establish boundaries of uncertainty, and validate whether findings are statistically significant or just random chance.

### Important Definitions
- **Standard Deviation:** A measure of the dispersion or spread of values in a dataset.
- **T-Test:** A statistical test used to determine if there is a significant difference between the means of groups.
- **P-Value:** The probability of obtaining results at least as extreme as the observed results, assuming the null hypothesis is true.

### Best Practices
- Never use a statistical test without verifying its mathematical assumptions (e.g., normal distribution).
- Avoid "p-hacking" — repeating tests on subgroups to find a favorable result.

### Common Mistakes
- Treating correlation as causation.
- Interpreting a high p-value as proof that the null hypothesis is true (we only "fail to reject" H0).

### Tips & Warnings
> 💡 **Tip:** Standard deviation depends on degrees of freedom. In Python, use `ddof=1` for sample standard deviation.
""",
        "instructions": """#### What you will do:
You will calculate statistical measures and perform a t-test to evaluate a null hypothesis.

#### Step-by-Step Instructions:
1. **Step 1:** Run the script and observe the printed mean, median, standard deviation, and p-value.
2. **Step 2:** Modify the target population mean parameter `popmean=15` in `ttest_1samp` to `popmean=13.5`.
3. **Step 3:** Run the script again. Compare how the p-value changes when the expected mean is closer to the sample mean.
""",
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
        "expected_outcomes": """### Knowledge Outcomes
- Explain the difference between supervised learning (classification vs regression) and unsupervised learning.
- Define overfitting and explain why a train/test split is necessary.
- Select appropriate evaluation metrics for model performance.

### Practical Outcomes
- Load standardized datasets from scikit-learn.
- Partition datasets into training (80%) and testing (20%) sets.
- Instantiate and fit a Random Forest classifier.
- Calculate and evaluate model accuracy.

### Industry-Relevant Skills
- Deploying baseline predictive models to automate classifications (e.g., spam filtering, client churn predictions).
""",
        "learning_notes": """### Concept Explanation & Theory
Machine learning is the study of computer algorithms that improve automatically through experience. In supervised learning, the model is trained on labeled training data to learn mapping functions.

### Important Definitions
- **Supervised Learning:** Training models using labeled target features.
- **Overfitting:** When a model performs exceptionally well on training data but poorly on unseen test data.
- **Random Forest:** An ensemble method that trains multiple decision trees and aggregates their predictions.

### Best Practices
- Always use a random state variable (`random_state`) to ensure reproducibility when splitting data.
- Scale features if the algorithm is sensitive to magnitude (like SVM or KNN).

### Common Mistakes
- Data leakage: letting testing details contaminate training steps.

### Tips & Warnings
> 💡 **Tip:** A baseline model should always be trained first to benchmark improvements.
""",
        "instructions": """#### What you will do:
You will split the classic Iris dataset, train a Random Forest, and output its test accuracy.

#### Step-by-Step Instructions:
1. **Step 1:** Run the script and observe the test accuracy.
2. **Step 2:** Change the split test size: change `test_size=0.2` to `test_size=0.4` (40% test data).
3. **Step 3:** Re-run and check if accuracy changed.
4. **Step 4:** Change the Random Forest number of trees: change `n_estimators=100` to `n_estimators=10`. Run again.
""",
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
        "expected_outcomes": """### Knowledge Outcomes
- Explain why time series data requires specialized ordering and indexing.
- Identify the differences between resampling (aggregating time) and rolling window (smoothing time) operations.
- Describe stationarity and autocorrelation at a high level.

### Practical Outcomes
- Set and sort datetime indices in Pandas DataFrames.
- Compute rolling moving averages to reveal underlying trends.
- Resample higher frequency data to monthly or quarterly figures.

### Industry-Relevant Skills
- Analyzing climate trends, forecasting malaria outbreaks, and predicting sales targets over fiscal quarters.
""",
        "learning_notes": """### Concept Explanation & Theory
A time series is a sequence of data points recorded at regular time intervals. Specialized techniques are required because temporal data violates the independence assumption of classical statistical models (i.e., today's value is correlated with yesterday's value).

### Important Definitions
- **Resampling:** Changing the frequency of time series observations (downsampling to monthly aggregates or upsampling to daily interpolations).
- **Rolling Window:** Computing stats (like mean) inside a moving window of a fixed window size.
- **Trend:** The long-term direction or progression of a time series.

### Best Practices
- Always ensure date columns are parsed as Datetime objects and set as the DataFrame index.
- Fill missing time steps carefully; use forward fill (`ffill`) or linear interpolation.

### Common Mistakes
- Forgetting to sort the time series index chronologically before performing rolling window tasks.

### Tips & Warnings
> 💡 **Tip:** Visualizing your time series is the most effective diagnostic step before starting analysis.
""",
        "instructions": """#### What you will do:
You will calculate rolling averages on simulated sales figures over a date range.

#### Step-by-Step Instructions:
1. **Step 1:** Run the script and review the rolling averages.
2. **Step 2:** Change the rolling window size from `window=3` to `window=2`.
3. **Step 3:** Change the frequency of dates from monthly `freq='M'` to weekly `freq='W'`.
4. **Step 4:** Run again and observe changes.
""",
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
