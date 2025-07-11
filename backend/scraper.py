import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

def scrape_amazon(query):
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/114.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options)
    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    products = []
    for item in soup.select(".s-result-item[data-component-type='s-search-result']"):
        title = item.select_one("h2 a span")
        link = item.select_one("h2 a")
        price = item.select_one(".a-price .a-offscreen")
        image = item.select_one(".s-image")

        if title and link and price and image:
            products.append({
                "title": title.get_text(strip=True),
                "link": "https://www.amazon.in" + link["href"],
                "price": price.get_text(strip=True),
                "image": image["src"]
            })

    print(f"[OK] Found {len(products)} products for query: {query}")
    return products
