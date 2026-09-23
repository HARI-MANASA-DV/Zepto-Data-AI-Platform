# Capstone Project

This repository contains my capstone project with three modules:

* `data_pipeline` – scraping, cleaning, database and data analysis
* `analytics` – Titanic dataset analysis and machine learning
* `support_assistant` – a simple Zepto policy support assistant

## Project Structure

```text
.
├── .gitignore
├── README.md
├── data_pipeline/
├── analytics/
└── support_assistant/
```

## 1. Data Pipeline

This module works with book data from Books to Scrape.

The main steps are:

1. Scrape the first 5 pages of the website.
2. Collect 100 books.
3. Clean the data.
4. Convert the price from GBP to INR.
5. Store the data in SQLite.
6. Run SQL queries.
7. Perform similar analysis using Pandas.
8. Compare SQL JOIN results with Pandas merge.

Main files include:

* `scrape_pipeline.py`
* `clean_data.py`
* `database.py`
* `queries.py`
* `pandas_analysis.py`

The module also contains the raw and cleaned CSV files, SQLite database and query output.

For more details, see [`data_pipeline/README.md`](data_pipeline/README.md).

## 2. Analytics

This module uses the Titanic dataset for EDA and machine learning.

### EDA

The analysis includes:

* Dataset information and missing values
* Data cleaning
* Age and fare analysis
* Survival analysis
* Multivariate analysis
* Correlation analysis
* Standardization for EDA
* Charts and visualizations

### Machine Learning

The classification models used are:

* Logistic Regression
* Decision Tree
* Random Forest
* Tuned Random Forest

The models are evaluated using accuracy, precision, recall, F1 score and ROC-AUC.

I also tested two ways of handling class imbalance:

* Class weights
* SMOTE

For regression, I used Multivariate Linear Regression to predict fare.

The regression metrics are:

* MAE
* RMSE
* R²
* Adjusted R²

The saved best pipeline is:

```text
analytics/best_pipeline.joblib
```

The notebooks are:

```text
01_eda.ipynb
02_modeling.ipynb
```

For more details, see [`analytics/README.md`](analytics/README.md).

## 3. Support Assistant

This module is a simple support assistant based on Zepto policy documents.

It uses 8 local policy documents and stores their embeddings in ChromaDB.

The main flow is:

```text
User Query
   ↓
Intent Classification
   ↓
Policy Question?
   ↓
Retrieve Relevant Document
   ↓
Generate Structured Response
```

The project uses:

* ChromaDB
* Sentence Transformers
* LangGraph
* Pydantic
* FastAPI
* Docker

The assistant can also run in offline mock mode.

For more details, see [`support_assistant/README.md`](support_assistant/README.md).

## Technologies

Python, Pandas, NumPy, SQLite, Seaborn, Matplotlib, Scikit-learn, imbalanced-learn, ChromaDB, LangGraph, FastAPI and Docker.

## Running the Project

Each module has its own `requirements.txt` file and README with the commands needed to run it.

This repository is intended to be submitted as **one GitHub repository containing all three modules**.
