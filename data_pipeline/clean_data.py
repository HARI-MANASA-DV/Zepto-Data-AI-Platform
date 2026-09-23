import pandas as pd


# Required project-defined conversion rate
GBP_TO_INR = 105.50


def clean_data():

    # Read the raw scraped data
    df = pd.read_csv("data_pipeline/raw_books.csv")

    # --------------------------------------------------
    # 1. Clean price
    # --------------------------------------------------

    # Remove the £ symbol and convert to numeric
    df["price_gbp"] = (df["price"].str.extract(r"(\d+(?:\.\d+)?)", expand=False))


    df["price_gbp"] = pd.to_numeric(
        df["price_gbp"],
        errors="coerce"
    )

    # Median imputation for invalid/missing numeric prices
    price_median = df["price_gbp"].median()

    df["price_gbp"] = df["price_gbp"].fillna(price_median)

    # --------------------------------------------------
    # 2. Convert star rating text to integer
    # --------------------------------------------------

    rating_mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    df["rating"] = df["star_rating"].map(rating_mapping)

    # Median imputation for unexpected rating values
    rating_median = int(df["rating"].median())

    df["rating"] = df["rating"].fillna(rating_median).astype(int)

    # --------------------------------------------------
    # 3. Convert availability to boolean
    # --------------------------------------------------

    df["in_stock"] = df["availability"].str.contains(
        "In stock",
        case=False,
        na=False
    )

    # --------------------------------------------------
    # 4. Convert GBP to INR
    # --------------------------------------------------

    df["price_inr"] = df["price_gbp"] * GBP_TO_INR

    # --------------------------------------------------
    # 5. Select final columns
    # --------------------------------------------------

    df = df[
        [
            "title",
            "price_gbp",
            "price_inr",
            "rating",
            "in_stock",
            "category"
        ]
    ]

    return df


if __name__ == "__main__":

    df = clean_data()

    print("\nCleaning completed!")

    print("\nData types:")
    print(df.dtypes)

    print("\nFirst 5 cleaned rows:")
    print(df.head().to_string())

    print("\nNumber of rows:")
    print(len(df))

    # Save cleaned dataset
    df.to_csv(
        "data_pipeline/cleaned_books.csv",
        index=False
    )

    print(
        "\nCleaned data saved to "
        "data_pipeline/cleaned_books.csv"
    )