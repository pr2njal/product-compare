import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from urllib.parse import urljoin


def build_ajio_url(query: str, sort: str = "relevance") -> str:
    query_formatted = query.lower().replace(" ", "+")
    url = f"https://www.ajio.com/search/?text={query_formatted}"

    if sort == "price_low_high":
        url += "&sortBy=priceAsc"
    elif sort == "price_high_low":
        url += "&sortBy=priceDesc"

    return url


def clean_price(price_str):
    """Extract numeric value from price string like '₹1,574'."""
    if not price_str:
        return None
    match = re.search(r"\d+", price_str.replace(",", ""))
    return match.group() if match else None


def scrape_ajio(query, max_results=5, sort="relevance"):
    print(f"[INFO] Scraping top {max_results} products on Ajio for '{query}'...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=options)

    url = build_ajio_url(query, sort)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.item"))
        )

        # Scroll to load more products
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        product_elements = soup.select("div.item")

        results = []
        for elem in product_elements[:max_results]:
            title_tag = elem.select_one("div.brand, div.name")
            price_tag = elem.select_one("span.price") or elem.select_one("div.price")
            link_tag = elem.find("a", href=True)
            img_tag = elem.select_one("img")

            if not price_tag or not img_tag:
                continue

            title = " ".join(t.get_text(strip=True) for t in elem.select("div.brand, div.name")) or "No Title"
            price_raw = price_tag.get_text(strip=True).replace("Rs.", "₹").strip()
            price = clean_price(price_raw)

            if not price:
                continue

            link = urljoin("https://www.ajio.com", link_tag["href"]) if link_tag else None
            img = img_tag.get("src") or img_tag.get("data-src")

            results.append({
                "title": title,
                "price": price,
                "rating": "0",   # Ajio doesn’t show ratings
                "link": link,
                "image": img,
                "source": "ajio"
            })

        print(f"[OK] Scraped {len(results)} products for demo.")
        return results

    except Exception as e:
        print(f"[ERROR] Ajio scraping failed: {e}")
        return []

    finally:
        driver.quit()
