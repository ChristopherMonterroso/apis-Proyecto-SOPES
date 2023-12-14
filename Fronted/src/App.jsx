// src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleButtonClick = () => {
    const url = 'http://localhost:5000/api/social-media-info';
    const params = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(inputValue)
    };
    return fetch(url, params)
        .then(response => response.json())
        .then(data => data)
        .catch(error => console.error('Error:', error));
  };

  return (
    <div className="App">
      <h1>WEB SCRAPING</h1>
      <div className="container">
        <input
          type="text"
          placeholder="Ingresa algo..."
          value={inputValue}
          onChange={handleInputChange}
        />
        <button onClick={handleButtonClick}>Lanzar</button>
      </div>
    </div>
  );
}

export default App;
