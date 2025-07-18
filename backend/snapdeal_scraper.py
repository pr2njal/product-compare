import time
from bs4 import BeautifulSoup
import undetected_chromedriver as uc


def scrape_snapdeal(query):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options)
    url = f"https://www.snapdeal.com/search?keyword={query.replace(' ', '%20')}&sort=rlvncy"
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    results = soup.select("div.product-tuple-listing")

    products = []
    for item in results:
        try:
            title_tag = item.select_one("p.product-title")
            link_tag = item.select_one("a.dp-widget-link")
            price_tag = item.select_one("span.product-price")
            image_tag = item.select_one("img.product-image")

            if title_tag and link_tag and price_tag and image_tag:
                title = title_tag.get_text(strip=True)
                link = link_tag["href"]
                price = price_tag.get_text(strip=True).replace("Rs. ", "")
                image = image_tag["src"]

                products.append({
                    "title": title,
                    "link": link,
                    "price": price,
                    "image": image,
                     "source": "snapdeal"

                })
        except Exception as e:
            print(f"[WARN] Skipping item due to error: {e}")

    print(f"[OK] Found {len(products)} products on Snapdeal for query: {query}")
    return products
