# Data Pipeline

This module is about collecting book data, cleaning it, storing it in a database and doing some analysis.

## What I Did

I used Books to Scrape as the source.

The pipeline does the following:

1. Scrapes the first 5 pages.
2. Collects 100 books.
3. Saves the raw data to `raw_books.csv`.
4. Cleans the data.
5. Converts the price from GBP to INR using `1 GBP = 105.50 INR`.
6. Saves the cleaned data to `cleaned_books.csv`.
7. Stores the data in SQLite.
8. Runs SQL queries.
9. Performs similar analysis using Pandas.
10. Compares SQL JOIN with `pandas.merge()`.

## Files

* `scrape_pipeline.py` – collects the book data
* `clean_data.py` – cleans the scraped data
* `database.py` – creates and loads the SQLite database
* `queries.py` – SQL queries and analysis
* `pandas_analysis.py` – Pandas analysis
* `raw_books.csv` – raw scraped data
* `cleaned_books.csv` – cleaned data
* `books.db` – SQLite database
* `sql_query_outputs.txt` – saved SQL results

## Database

The database contains two main tables:

* `categories`
* `books`

The `books` table is connected to `categories` using a foreign key.

## Run the Module

Install the required packages:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python scrape_pipeline.py
python clean_data.py
python database.py
python queries.py
python pandas_analysis.py
```

## Result

The module produces the scraped dataset, cleaned dataset, SQLite database and SQL analysis output.
