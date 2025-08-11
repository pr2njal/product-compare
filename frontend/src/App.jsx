import { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [sortOption, setSortOption] = useState('relevance');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setProducts([]);

    try {
      const response = await fetch(
        `http://localhost:5000/search?q=${encodeURIComponent(query)}&source=all&sort=${sortOption}`
      );
      const data = await response.json();

      if (!data || data.length === 0) {
        setError('No products found.');
      } else {
        setProducts(data);
      }
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch product data.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>Product Aggregator App</h1>

      {/* Search Bar */}
      <div className="search-bar">
        <input
          type="text"
          placeholder="Enter product name..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        {/* Sorting options */}
        <select
          value={sortOption}
          onChange={(e) => setSortOption(e.target.value)}
        >
          <option value="relevance">Relevance</option>
          <option value="price_low_high">Price: Low to High</option>
          <option value="price_high_low">Price: High to Low</option>
          <option value="rating_high_low">Rating: High to Low</option>
        </select>

        <button onClick={handleSearch}>Search</button>
      </div>

      {/* Loading Spinner */}
      {loading && (
        <div className="loader-container">
          <div className="spinner"></div>
          <p>Fetching products...</p>
        </div>
      )}

      {/* Error Message */}
      {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

      {/* Product List */}
      <div className="product-list">
        {products.map((product, idx) => (
          <div className="product-card" key={idx}>
            <img src={product.image} alt={product.title} />
            <h3>{product.title}</h3>
            <p>Price: {product.price}</p>
            <p>Source: {product.source}</p>
            <a
              href={product.link}
              target="_blank"
              rel="noopener noreferrer"
            >
              View Product
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
