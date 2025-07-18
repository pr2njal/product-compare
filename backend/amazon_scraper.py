import time
from bs4 import BeautifulSoup
import undetected_chromedriver as uc


def scrape_amazon(query):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options)
    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    driver.get(url)
    time.sleep(5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    results = soup.select(".s-result-item[data-component-type='s-search-result']")
    print(f"[DEBUG] Found {len(results)} result containers for query: {query}\n")

    products = []
    for item in results:
        try:
            # Primary and fallback selectors for title and link
            title_tag = item.select_one("h2 span.a-text-normal") or item.select_one("h2 span")
            link_tag = item.select_one("a.a-link-normal.s-no-outline") or item.select_one("a.a-link-normal.a-text-normal")
            price_whole = item.select_one("span.a-price-whole")
            price_fraction = item.select_one("span.a-price-fraction")
            image_tag = item.select_one("img.s-image")

            # Debug output
            print("------------")
            print("TITLE:", title_tag.get_text(strip=True) if title_tag else "None")
            print("LINK:", link_tag['href'] if link_tag else "None")
            print("PRICE WHOLE:", price_whole.get_text(strip=True) if price_whole else "None")
            print("PRICE FRACTION:", price_fraction.get_text(strip=True) if price_fraction else "None")
            print("IMAGE:", image_tag['src'] if image_tag else "None")

            if title_tag and link_tag and price_whole and image_tag:
                title = title_tag.get_text(strip=True)
                link = "https://www.amazon.in" + link_tag["href"]
                price = price_whole.get_text(strip=True)
                if price_fraction:
                    price += "." + price_fraction.get_text(strip=True)
                image = image_tag["src"]

                products.append({
                    "title": title,
                    "link": link,
                    "price": price,
                    "image": image,
                     "source": "amazon"
                })
        except Exception as e:
            print(f"[WARN] Skipping item due to error: {e}")

    print(f"\n[OK] Found {len(products)} products for query: {query}")
    return products
