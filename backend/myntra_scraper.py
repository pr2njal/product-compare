import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from urllib.parse import urljoin   # ✅ new import


def build_myntra_url(query: str, sort: str = "relevance") -> str:
    query_formatted = query.lower().replace(" ", "-")
    url = f"https://www.myntra.com/{query_formatted}"

    if sort == "price_low_high":
        url += "?sort=price_asc"
    elif sort == "price_high_low":
        url += "?sort=price_desc"

    return url


def clean_price(price_str):
    """Extract numeric value from a price string like '₹1,574' or 'Rs. 351'."""
    if not price_str:
        return None
    match = re.search(r"\d+", price_str.replace(",", ""))
    return match.group() if match else None


def scrape_myntra(query, max_results=5, sort="relevance"):
    print(f"[INFO] Scraping top {max_results} products on Myntra for '{query}'...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=options)

    url = build_myntra_url(query, sort)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-base"))
        )

        # Only scroll once for demo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        product_elements = soup.select("li.product-base")

        results = []
        for elem in product_elements[:max_results]:
            title_tag = elem.select_one("h3")
            price_tag = elem.select_one("span.product-discountedPrice") or elem.select_one("span.product-basePrice")
            link_tag = elem.find("a")
            img_tag = elem.select_one("img")

            if not img_tag or not price_tag:
                continue  # 🚀 Skip products without price or image

            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            price_raw = price_tag.get_text(strip=True).replace("Rs.", "₹").strip()
            price = clean_price(price_raw)

            if not price:
                continue  # 🚀 Skip if clean_price fails

            # ✅ Fix link handling
            link = urljoin("https://www.myntra.com", link_tag["href"]) if link_tag else None
            img = img_tag.get("src") or img_tag.get("data-src")

            results.append({
                "title": title,
                "price": price,      # ✅ Always numeric string
                "rating": "0",       # Myntra doesn’t always show rating
                "link": link,
                "image": img,
                "source": "myntra"
            })

        print(f"[OK] Scraped {len(results)} products for demo.")
        return results

    except Exception as e:
        print(f"[ERROR] Myntra scraping failed: {e}")
        return []

    finally:
        driver.quit()
