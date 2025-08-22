from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_snapdeal
from scraper import scrape_myntra
from scraper import scrape_ajio
from models import db, Product
from sqlalchemy import true
import os
import re

app = Flask(__name__)
CORS(app)

# SQLite config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Run once to create the database
with app.app_context():
    db.create_all()


def normalize_search_term(term):
    term = term.lower()
    term = re.sub(r'[^a-z0-9]', '', term)  # Remove spaces, hyphens, special chars
    return term


def extract_base_keyword(query):
    base_keywords = ['tshirt', 'shirt', 'jeans', 'shoes']  # Add your categories here
    for base in base_keywords:
        if base in query:
            return base
    return query  # fallback to whole query if no base keyword found


def sort_products(product_list, sort_option):
    def parse_price(price_str):
        try:
            return float(price_str.replace(",", "").replace("₹", "").strip())
        except:
            return float('inf')

    def parse_rating(rating_str):
        try:
            return float(rating_str.split()[0])
        except:
            return 0.0

    try:
        if sort_option == "price_low_high":
            product_list.sort(key=lambda x: parse_price(x.get("price", "inf")))
        elif sort_option == "price_high_low":
            product_list.sort(key=lambda x: parse_price(x.get("price", "0")), reverse=True)
        elif sort_option == "rating_high_low":
            product_list.sort(key=lambda x: parse_rating(x.get("rating", "0")), reverse=True)
    except Exception as e:
        print(f"[WARN] Sorting failed: {e}")

    return product_list


@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    source = request.args.get("source", "all").lower()
    sort_option = request.args.get("sort", "relevance").lower()

    if not query:
        return jsonify({"error": "Missing search query"}), 400

    normalized_query = normalize_search_term(query)
    base_keyword = extract_base_keyword(normalized_query)

    # Step 1: Find products for base keyword from DB
    base_results = Product.query.filter_by(search_keyword=base_keyword).all()
    source_filtered = [p for p in base_results if (p.source == source or source == "all")]

    # Step 2: Filter products for all query words in title
    if source_filtered:
        query_words = query.split()
        filtered_products = []
        for product in source_filtered:
            title_lower = product.title.lower()
            if all(word in title_lower for word in query_words) or product.search_keyword == base_keyword:
                   filtered_products.append(product)


        if filtered_products:
            print(f"[INFO] Returning {len(filtered_products)} filtered products from DB for query '{query}'")
            product_list = [{
                'title': p.title,
                'price': p.price,
                'rating': p.rating,
                'link': p.link,
                'image': p.image,
                'source': p.source
            } for p in filtered_products]

            product_list = sort_products(product_list, sort_option)
            return jsonify(product_list)

    # Step 3: If no filtered results, scrape from sources
    print(f"[INFO] No filtered results found, scraping for '{query}'")
    scraped_results = []

    if source in ["all", "snapdeal"]:
        try:
            results = scrape_snapdeal(query)
            print(f"[DEBUG] Snapdeal scraped {len(results)} products.")
            scraped_results.extend(results)
        except Exception as e:
            print(f"[ERROR] Snapdeal scrape failed: {e}")

    if source in ["all", "myntra"]:
        try:
            results = scrape_myntra( query)
            print(f"[DEBUG] Myntra scraped {len(results)} products.")
            scraped_results.extend(results)
        except Exception as e:
            print(f"[ERROR] Myntra scrape failed: {e}")
            
    if source in ["all", "ajio"]:   # 👈 add this block
        try:
            results = scrape_ajio(query)
            print(f"[DEBUG] Ajio scraped {len(results)} products.")
            scraped_results.extend(results)
        except Exception as e:
            print(f"[ERROR] Ajio scrape failed: {e}")        

   
    # Deduplicate by product link
    unique_links = set()
    unique_results = []
    for item in scraped_results:
        if item['link'] not in unique_links:
            unique_links.add(item['link'])
            unique_results.append(item)
    scraped_results = unique_results

    # Save scraped results with base_keyword in DB
    try:
        for item in scraped_results:
            existing = Product.query.filter_by(title=item["title"], link=item["link"]).first()
            if not existing:
                product = Product(
                    title=item["title"],
                    price=item["price"],
                    rating=item.get("rating", "0"),
                    link=item["link"],
                    image=item["image"],
                    source=item["source"],
                    search_keyword=base_keyword
                )
                db.session.add(product)
        db.session.commit()
    except Exception as e:
        print(f"[WARN] DB save failed: {e}")

    scraped_results = sort_products(scraped_results, sort_option)
    return jsonify(scraped_results)


if __name__ == "__main__":
    print("Starting Flask server on http://127.0.0.1:5000 ...")
    app.run(debug=True)
