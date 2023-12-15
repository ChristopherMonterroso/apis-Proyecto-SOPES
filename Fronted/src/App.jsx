// src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleButtonClick = () => {
    const fetchData = async (url) => {
      const jsonData = {
        "url": inputValue
      };

      const params = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
      };

      try {
        const response = await fetch(url, params);
        return await response.json();
      } catch (error) {
        return console.error('Error:', error);
      }
    };

    // Lista de URLs que deseas consultar
    const urls = ['http://localhost:5001/api/domain-social-info', 'http://127.0.0.1:7001/api/domain-social-info'];

    // Realizar solicitudes en paralelo
    Promise.all(urls.map(url => fetchData(url)))
      .then(dataArray => {
        // Aquí dataArray contiene los resultados de ambas solicitudes
        const result1 = dataArray[0];
        const result2 = dataArray[1];
        console.log('Resultado 1:', result1);
        console.log('Resultado 2:', result2);
      })
      .catch(error => console.error('Error en alguna de las solicitudes:', error));
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
