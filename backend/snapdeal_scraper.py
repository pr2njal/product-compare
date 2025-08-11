import time
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_snapdeal(query):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36"
    )

    products = []
    try:
        driver = uc.Chrome(options=options)
        url = f"https://www.snapdeal.com/search?keyword={query.replace(' ', '%20')}&sort=rlvncy"
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-tuple-listing"))
            )
        except:
            print(f"[WARN] No products loaded for query: {query}")
            driver.quit()
            return []

        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.select("div.product-tuple-listing")

        for item in results:
            try:
                title_tag = item.select_one("p.product-title")
                link_tag = item.select_one("a.dp-widget-link")
                price_tag = item.select_one("span.product-price")
                image_tag = item.select_one("img.product-image")
                rating_tag = item.select_one("div.filled-stars")  # Snapdeal shows rating as % width sometimes

                if title_tag and link_tag and price_tag and image_tag:
                    title = title_tag.get_text(strip=True)
                    link = link_tag["href"]
                    price = "₹" + price_tag.get_text(strip=True).replace("Rs. ", "").replace(",", "")
                    image = image_tag.get("src") or image_tag.get("data-src")
                    if image and image.startswith("//"):
                        image = "https:" + image

                    rating = "0"
                    if rating_tag and rating_tag.get("style"):
                        try:
                            percent = float(rating_tag.get("style").split(":")[1].replace("%", "").strip())
                            rating = str(round((percent / 20), 1))  # Convert % to 5-star scale
                        except:
                            pass

                    products.append({
                        "title": title,
                        "link": link,
                        "price": price,
                        "image": image,
                        "rating": rating,
                        "source": "snapdeal"
                    })
            except Exception as e:
                print(f"[WARN] Skipping item due to error: {e}")

        print(f"[OK] Found {len(products)} products on Snapdeal for query: {query}")
    except Exception as e:
        print(f"[ERROR] Snapdeal scrape failed: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

    return products
