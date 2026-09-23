import requests
from bs4 import BeautifulSoup
import pandas as pd


BASE_URL = "https://books.toscrape.com/"
PAGES_TO_SCRAPE = 5


def scrape_books():
    books = []

    for page in range(1, PAGES_TO_SCRAPE + 1):

        if page == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}catalogue/page-{page}.html"

        response = requests.get(url)

        print(f"Scraping page {page}: {url}")
        print(f"Status code: {response.status_code}")

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        book_items = soup.select("article.product_pod")

        for book in book_items:

            title = book.h3.a["title"]

            price = book.select_one(".price_color").text.strip()

            rating_class = book.select_one("p.star-rating")["class"]
            star_rating = rating_class[1]

            availability = book.select_one(".availability").text.strip()

            book_link = book.h3.a["href"]

            # Convert relative URL into absolute URL
            book_url = requests.compat.urljoin(url, book_link)

            # Open individual book page to get category
            book_response = requests.get(book_url)
            book_response.raise_for_status()

            book_soup = BeautifulSoup(book_response.text, "html.parser")

            category = book_soup.select(
                "ul.breadcrumb li a"
            )[-1].text.strip()

            books.append({
                "title": title,
                "price": price,
                "star_rating": star_rating,
                "availability": availability,
                "category": category
            })

    return pd.DataFrame(books)

if __name__ == "__main__":

    df = scrape_books()

    print("\nScraping completed!")
    print(f"Total books scraped: {len(df)}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nCategories:")
    print(df["category"].value_counts())

    # Save raw scraped data
    df.to_csv("data_pipeline/raw_books.csv", index=False)

    print("\nRaw data saved to data_pipeline/raw_books.csv")