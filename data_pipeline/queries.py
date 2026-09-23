import sqlite3
import pandas as pd
from pathlib import Path

DATABASE_PATH = "data_pipeline/books.db"
OUTPUT_PATH = Path("data_pipeline/sql_query_outputs.txt")

# Connect to database
conn = sqlite3.connect(DATABASE_PATH)

# Enable foreign keys
conn.execute("PRAGMA foreign_keys = ON")
output_file = open(OUTPUT_PATH, "w", encoding="utf-8")

# ==========================================================
# Query 1 — SELECT + WHERE
# ==========================================================

query1 = """
SELECT title, price_gbp, rating, in_stock
FROM books
WHERE rating >= 4;
"""

result1 = pd.read_sql(query1, conn)

print("\n========== QUERY 1 ==========")
print(query1)
print("OUTPUT:")
print(result1.to_string(index=False))
output_file.write("\n========== QUERY 1 ==========\n")
output_file.write(query1)
output_file.write("\nOUTPUT:\n")
output_file.write(result1.to_string(index=False))
output_file.write("\n")

# ==========================================================
# Query 2 — ORDER BY + LIMIT
# ==========================================================

query2 = """
SELECT title, price_gbp, price_inr
FROM books
ORDER BY price_gbp DESC
LIMIT 10;
"""

result2 = pd.read_sql(query2, conn)

print("\n========== QUERY 2 ==========")
print(query2)
print("OUTPUT:")
print(result2.to_string(index=False))


# ==========================================================
# Query 3 — DISTINCT
# ==========================================================

query3 = """
SELECT DISTINCT category_name
FROM categories
ORDER BY category_name;
"""

result3 = pd.read_sql(query3, conn)

print("\n========== QUERY 3 ==========")
print(query3)
print("OUTPUT:")
print(result3.to_string(index=False))


# ==========================================================
# Query 4 — BETWEEN
# ==========================================================

query4 = """
SELECT title, price_gbp, rating
FROM books
WHERE price_gbp BETWEEN 20 AND 30
ORDER BY price_gbp;
"""

result4 = pd.read_sql(query4, conn)

print("\n========== QUERY 4 ==========")
print(query4)
print("OUTPUT:")
print(result4.to_string(index=False))


# ==========================================================
# Query 5 — IN
# ==========================================================

query5 = """
SELECT title, category_id, rating
FROM books
WHERE category_id IN (1, 2, 3)
ORDER BY rating DESC;
"""

result5 = pd.read_sql(query5, conn)

print("\n========== QUERY 5 ==========")
print(query5)
print("OUTPUT:")
print(result5.to_string(index=False))


# ==========================================================
# Query 6 — JOIN
# ==========================================================

query6 = """
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

result6 = pd.read_sql(query6, conn)

print("\n========== QUERY 6 ==========")
print(query6)
print("OUTPUT:")
print(result6.to_string(index=False))

output_file.close()

print(f"\nSQL query outputs saved to {OUTPUT_PATH}")

# Close database connection
conn.close()