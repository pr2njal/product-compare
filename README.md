# Product Aggregation App

## Overview

The Product Aggregation App is a web-based tool that helps users search for products across multiple e-commerce websites and view all relevant results in one place. No more hopping from site to site — find the best deals, prices, and ratings aggregated and displayed conveniently on a single platform.

---

## Features

- **Multi-site scraping:** Aggregates products from popular e-commerce platforms like Snapdeal (and more sites to be added soon).  
- **Database integration:** Stores previously searched products in a database to deliver faster results and reduce redundant scraping.  
- **Smart search filtering:** Supports keyword filtering within stored product results to refine your searches (e.g., searching "pink tshirt" filters stored "tshirt" products).  
- **Sorting options:** Sort results by price (low to high, high to low) or rating.  
- **RESTful API:** Provides a simple JSON API to query products by keyword, source, and sorting preferences.  
- **Extensible architecture:** Easily add more e-commerce sites to expand product coverage.

---

## Technologies Used

- **Backend:** Python, Flask, Flask-SQLAlchemy  
- **Database:** SQLite (lightweight and easy to set up)  
- **Web Scraping:** BeautifulSoup, undetected-chromedriver  
- **Frontend:** HTML, CSS, JavaScript (optional - for UI polishing branch)  

---

## Installation & Setup

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/product-compare.git
   cd product-compare
   
