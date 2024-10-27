import React, { useState,useEffect } from 'react';
import './style.css';
import './Shop.css'; // Import a CSS file for styling

const Shop = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Fetch results based on user input
    const fetchedResults = await fetchResults(query);
    setResults(fetchedResults);
  };

  const fetchResults = async (query) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/scrape?query=${query}`);
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      return data; // Adjust according to your API response structure
    } catch (error) {
      console.error('Fetch error:', error);
      return [];
    }
  };

    // Use useEffect to run the scraper when the component mounts
    useEffect(() => {
        const fetchInitialResults = async () => {
          if (query) {
            await fetchResults(query); // Run the scraper with the initial query
          }
        };
    
        fetchInitialResults(); // Call the function
      }, []); // Empty dependency array means it runs once on mount

  return (
    <>
    <nav className="navbar">
    <div className="container-fluid">
      <a className="navbar-brand text-center" href="#">NutriPass</a>
      <form className="search-group" onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={handleChange}
          placeholder="Enter your search query"
          className="form-control form-control-lg"
        />
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
      
    </div>
    </nav>
    <div>
      <h1>Shop Page</h1>

      <div className="results">
        <h2>Results:</h2>
        <div className="card-container">
          {results.map((item, index) => (
                <div className="card" key={index} >
                    <img src={item.thumbnail_url} className="card-img-top" alt={item.product_name}/>
                    <div class="card-body">
                        <h5 className="card-title">{item.product_name}</h5>
                        <p className="card-text">Price: ${item.product_price}</p>
                    </div>
                </div>
          ))}
        </div>
      </div>
    </div>
    <footer>Aby Huerta 2024</footer>
    </>
  );
};

export default Shop;
