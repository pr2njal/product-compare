import { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [products, setProducts] = useState([]);

  // Shuffle function to randomize the product order
  function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      const response = await fetch(`http://localhost:5000/search?q=${encodeURIComponent(query)}`);
      const data = await response.json();

      const shuffled = shuffleArray(data || []);
      setProducts(shuffled);
    } catch (error) {
      console.error('Error fetching data:', error);
      alert('Failed to fetch product data.');
    }
  };

  return (
    <div className="app-container">
      <h1>Product Aggregator App</h1>

      <div className="search-bar">
        <input
          type="text"
          placeholder="Enter product name..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      <div className="product-list">
        {products.map((product, idx) => (
          <div className="product-card" key={idx}>
            <img src={product.image} alt={product.title} />
            <h3>{product.title}</h3>
            <p>Price: {product.price}</p>
            <p>Source: {product.source}</p>
            <a
              href={product.link.startsWith('http') ? product.link : `https://www.amazon.in${product.link}`}
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
