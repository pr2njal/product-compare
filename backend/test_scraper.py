# test_scraper.py
from backend.amazon_scraper import scrape_amazon

query = "shirt"
results = scrape_amazon(query)

for i, product in enumerate(results, 1):
    print(f"\nProduct {i}:")
    print("Title:", product["title"])
    print("Price:", product["price"])
    print("Link:", product["link"])
    print("Image:", product["image"])
