async function search() {
  const query = document.getElementById("searchInput").value;
  if (!query) return alert("Enter a product name!");

  const response = await fetch(`http://127.0.0.1:5000/search?q=${query}`);
  const products = await response.json();

  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = ""; // Clear previous results

  products.forEach(product => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <img src="${product.image}" alt="${product.title}" />
      <h3>${product.title}</h3>
      <p>₹ ${product.price}</p>
      <p>Source: ${product.source}</p>
      <a href="${product.link}" target="_blank">View</a>
    `;
    resultsDiv.appendChild(card);
  });
}
