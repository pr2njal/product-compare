from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_amazon  # ✅ update this line

app = Flask(__name__)
CORS(app)

@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing search query"}), 400

    products = scrape_amazon(query)  # ✅ use amazon scraper
    return jsonify(products)

# ✅ This part is REQUIRED to run the server
if __name__ == "__main__":
    print("Starting Flask server...")  # Optional debug print
    app.run(debug=True)

