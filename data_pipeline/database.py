import sqlite3
import pandas as pd


DATABASE_PATH = "data_pipeline/books.db"


def create_database():

    # Read cleaned data
    df = pd.read_csv("data_pipeline/cleaned_books.csv")

    # Connect to SQLite database
    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    # Enable foreign key enforcement
    cursor.execute("PRAGMA foreign_keys = ON")

    # Remove existing tables so the database can be recreated
    # from scratch every time the script runs.
    cursor.execute("DROP TABLE IF EXISTS books")
    cursor.execute("DROP TABLE IF EXISTS categories")

    # --------------------------------------------------
    # Create categories table
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        )
    """)

    # --------------------------------------------------
    # Create books table
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price_gbp REAL NOT NULL,
            price_inr REAL NOT NULL,
            rating INTEGER NOT NULL,
            in_stock INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id)
                REFERENCES categories(category_id)
        )
    """)

    # --------------------------------------------------
    # Insert categories
    # --------------------------------------------------

    categories = sorted(df["category"].unique())

    for category in categories:
        cursor.execute(
            """
            INSERT INTO categories (category_name)
            VALUES (?)
            """,
            (category,)
        )

    # --------------------------------------------------
    # Insert books
    # --------------------------------------------------

    for _, row in df.iterrows():

        cursor.execute(
            """
            SELECT category_id
            FROM categories
            WHERE category_name = ?
            """,
            (row["category"],)
        )

        category_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO books (
                title,
                price_gbp,
                price_inr,
                rating,
                in_stock,
                category_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["title"],
                row["price_gbp"],
                row["price_inr"],
                row["rating"],
                int(row["in_stock"]),
                category_id
            )
        )

    conn.commit()

    # --------------------------------------------------
    # Verify database
    # --------------------------------------------------

    category_count = cursor.execute(
        "SELECT COUNT(*) FROM categories"
    ).fetchone()[0]

    book_count = cursor.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    print(f"Categories inserted: {category_count}")
    print(f"Books inserted: {book_count}")

    # Close connection
    conn.close()

    print(f"\nDatabase created successfully: {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()