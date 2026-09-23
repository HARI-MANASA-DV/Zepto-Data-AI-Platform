# Capstone Project

This repository contains my capstone project with three modules:

* `data_pipeline` – scraping, cleaning, SQLite and data analysis
* `analytics` – Titanic EDA and machine learning
* `support_assistant` – Zepto policy support assistant

## Repository Structure

```text
.
├── .gitignore
├── README.md
├── data_pipeline/
├── analytics/
└── support_assistant/
```

## Setup

I used **separate `requirements.txt` files for each module**. There is no single consolidated requirements file.

Install the requirements for the module you want to run.

## 1. Data Pipeline

### What I did

I collected book data from Books to Scrape.

The pipeline:

1. Scrapes the first 5 pages.
2. Collects 100 books.
3. Saves the raw data.
4. Cleans the book data.
5. Converts GBP prices to INR using the fixed rate `1 GBP = 105.50 INR`.
6. Stores the cleaned data in SQLite.
7. Runs SQL queries.
8. Performs the analysis again using Pandas.
9. Compares the SQL JOIN result with `pandas.merge()`.

### Design decisions

I used separate `categories` and `books` tables instead of keeping the category name repeated in every book row. The relationship is maintained using a primary key and foreign key.

For parsing, the `£` symbol is removed from prices and the value is converted to numeric. Ratings such as `One`, `Two`, `Three`, `Four`, and `Five` are converted to integers from 1 to 5. Availability text is converted to a boolean `in_stock` value.

### Run

From the project root:

```bash
pip install -r data_pipeline/requirements.txt

python data_pipeline/scrape_pipeline.py
python data_pipeline/clean_data.py
python data_pipeline/database.py
python data_pipeline/queries.py
python data_pipeline/pandas_analysis.py
```

The module creates:

* `raw_books.csv`
* `cleaned_books.csv`
* `books.db`
* `sql_query_outputs.txt`

More details are available in [`data_pipeline/README.md`](data_pipeline/README.md).

## 2. Analytics

### What I did

I used the Titanic dataset for EDA and machine learning.

The EDA includes:

* Missing-value analysis
* Data cleaning
* Age and fare analysis
* Survival analysis
* Multivariate analysis
* Correlation analysis
* Standardization
* Visualizations

The machine-learning part includes:

* Logistic Regression
* Decision Tree
* Random Forest
* Tuned Random Forest
* Class-weight comparison
* SMOTE
* Multivariate Linear Regression

### Design decisions

I kept the raw Titanic dataset in `analytics/titanic.csv` as the offline fallback. The modeling notebook uses this saved CSV instead of loading the network dataset again.

The train/test split is stratified on the survival target and is done before preprocessing. Imputation, encoding and scaling are fitted only on the training data using pipelines.

The final fitted preprocessing and model pipeline is saved as:

```text
analytics/best_pipeline.joblib
```

### Run

Install the requirements:

```bash
pip install -r analytics/requirements.txt
```

Open and run the notebooks in this order:

```text
analytics/01_eda.ipynb
analytics/02_modeling.ipynb
```

The modeling notebook also reloads the saved pipeline and tests it on raw test rows.

More details are available in [`analytics/README.md`](analytics/README.md).

## 3. Support Assistant

### What I did

I built a Zepto policy assistant using 8 local policy documents.

The main flow is:

```text
Ingestion
   ↓
Embedding
   ↓
Retrieval
   ↓
Generation
```

### Design decisions

The policy documents are stored locally so that the basic version can work without a paid external service.

`ingest.py` creates embeddings using `all-MiniLM-L6-v2` and stores them in ChromaDB.

`rag.py` uses keyword-based intent classification and LangGraph to route policy and general questions.

The default `MOCK_LLM=1` mode does not make an external LLM call. Policy answers are generated from the top retrieved chunk, while unrelated questions use a fixed response.

The optional `MOCK_LLM=0` branch prepares the structured prompt for a real LLM path. `generate_with_retry()` is included to validate and retry an invalid structured response.

Pydantic is used to validate the final response, and FastAPI provides the `/ask` endpoint.

### Run

From the project root:

```bash
cd support_assistant
pip install -r requirements.txt
python ingest.py
python -m uvicorn main:app --host 0.0.0.0 --port 7860
```

Open:

```text
http://localhost:7860/docs
```

### Docker

From the `support_assistant` folder:

```bash
docker build -t zepto-support-assistant .
docker run --rm -p 7860:7860 zepto-support-assistant
```

Then open:

```text
http://localhost:7860/docs
```

More details are available in [`support_assistant/README.md`](support_assistant/README.md).

## Technologies

Python, Pandas, NumPy, SQLite, BeautifulSoup, Seaborn, Matplotlib, Scikit-learn, imbalanced-learn, ChromaDB, Sentence Transformers, LangGraph, Pydantic, FastAPI and Docker.

## Submission

This project is submitted as **one public GitHub repository** containing all three modules.
