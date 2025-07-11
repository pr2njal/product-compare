async function searchProducts() {
    const query = document.getElementById("searchInput").value;
  
    const response = await fetch(`http://127.0.0.1:5000/search?q=${encodeURIComponent(query)}`);
    const products = await response.json();
  
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";
  
    products.forEach(product => {
      const div = document.createElement("div");
      div.className = "product";
      div.innerHTML = `
        <img src="${product.image}" alt="Product Image"><br>
        <strong>${product.title}</strong><br>
        <span>${product.price}</span><br>
      `;
      resultsDiv.appendChild(div);
    });
  }
  
  