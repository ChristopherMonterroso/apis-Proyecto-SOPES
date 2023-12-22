// src/App.js
import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleButtonClick = () => {
    const postData = {
      url: inputValue
    };
    // Realizar la solicitud POST con Axios
    axios.post("http://localhost:9090/api/domain-social-info", postData, {
      headers: {
          'Content-Type': 'application/json'
          // Puedes agregar más encabezados si es necesario
      }
    })
    .then(response => {
      console.log('Respuesta del servidor:', response.data);
    })
    .catch(error => {
      console.error('Error en la solicitud:', error);
    });
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
