import sqlite3
import pandas as pd


DATABASE_PATH = "data_pipeline/books.db"


# Connect to SQLite database
conn = sqlite3.connect(DATABASE_PATH)


# ==========================================================
# 1. Read Query 1 result using pd.read_sql()
# ==========================================================

query1 = """
SELECT title, price_gbp, rating, in_stock
FROM books
WHERE rating >= 4;
"""

df_query1 = pd.read_sql(query1, conn)

print("\n========== pd.read_sql() - QUERY 1 ==========")
print(df_query1.head(10).to_string(index=False))


# ==========================================================
# 2. Read Query 2 result using pd.read_sql()
# ==========================================================

query2 = """
SELECT title, price_gbp, price_inr
FROM books
ORDER BY price_gbp DESC
LIMIT 10;
"""

df_query2 = pd.read_sql(query2, conn)

print("\n========== pd.read_sql() - QUERY 2 ==========")
print(df_query2.to_string(index=False))


# ==========================================================
# 3. Read the two database tables into DataFrames
# ==========================================================

books_df = pd.read_sql(
    "SELECT * FROM books",
    conn
)

categories_df = pd.read_sql(
    "SELECT * FROM categories",
    conn
)


print("\n========== BOOKS DATAFRAME ==========")
print(books_df.head().to_string(index=False))

print("\n========== CATEGORIES DATAFRAME ==========")
print(categories_df.head().to_string(index=False))


# ==========================================================
# 4. Reproduce JOIN using pandas merge()
# ==========================================================

merged_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)


# Select the same columns used by SQL JOIN query
merged_result = merged_df[
    [
        "title",
        "category_name",
        "rating",
        "price_gbp",
        "price_inr"
    ]
].sort_values(
    by=["rating", "price_gbp"],
    ascending=[False, False]
).head(10)


print("\n========== pandas.merge() JOIN RESULT ==========")
print(merged_result.to_string(index=False))


# ==========================================================
# 5. SQL JOIN result for comparison
# ==========================================================

join_query = """
SELECT
    b.title,
    c.category_name,
    b.rating,
    b.price_gbp,
    b.price_inr
FROM books b
JOIN categories c
    ON b.category_id = c.category_id
ORDER BY b.rating DESC, b.price_gbp DESC
LIMIT 10;
"""

sql_join_result = pd.read_sql(
    join_query,
    conn
)


print("\n========== SQL JOIN RESULT ==========")
print(sql_join_result.to_string(index=False))


# ==========================================================
# 6. Compare SQL JOIN and pandas merge()
# ==========================================================

sql_comparison = sql_join_result.reset_index(drop=True)

pandas_comparison = merged_result.reset_index(drop=True)

# Check whether both results are equivalent
are_equal = sql_comparison.equals(pandas_comparison)

print("\n========== COMPARISON ==========")
print(f"SQL JOIN and pandas merge() equivalent: {are_equal}")


# Close connection
conn.close()