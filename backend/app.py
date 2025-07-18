from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_amazon, scrape_snapdeal
import json

app = Flask(__name__)
CORS(app)

@app.route("/search")
def search():
    query = request.args.get("q")
    source = request.args.get("source", "all").lower()

    if not query:
        return jsonify({"error": "Missing search query"}), 400

    results = []

    if source == "amazon" or source == "all":
        try:
            amazon_products = scrape_amazon(query)
            results.extend(amazon_products)
        except Exception as e:
            print(f"[ERROR] Amazon scrape failed: {e}")

    if source == "snapdeal" or source == "all":
        try:
            snapdeal_products = scrape_snapdeal(query)
            results.extend(snapdeal_products)
        except Exception as e:
            print(f"[ERROR] Snapdeal scrape failed: {e}")

    # Optional: sort by price
    try:
        results.sort(key=lambda x: float(x["price"].replace(",", "").replace("₹", "")))
    except:
        print("[WARN] Could not sort by price")

    # Optional: save to JSON
    try:
        with open("results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[WARN] Could not save to file: {e}")

    return jsonify(results)

if __name__ == "__main__":
    print(" Starting Flask server on http://127.0.0.1:5000 ...")
    app.run(debug=True)
