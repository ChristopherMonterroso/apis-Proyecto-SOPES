
import React, { useState, useEffect } from 'react';

import './App.css';
const App = () => {
  const [stats_selenium, setStats] = useState(null);
  const [stats_playwright, setStats2] = useState(null);
  const [stats_redis, setStats3] = useState(null);
  const [stats_load_balancer, setStats4] = useState(null);


  const obtenerEstadisticas_selenium = async () => {
    try {
      const respuesta = await fetch('http://localhost:8010/container_selenium');
      console.log(respuesta)
      const datos = await respuesta.json();
      setStats(datos);

    } catch (error) {
      console.error('Error al obtener estadísticas:', error);
    }
  };
  const obtenerEstadisticas_playwright = async () => {
    try {
      const respuesta = await fetch('http://localhost:8010/container_playwright');
      console.log(respuesta)
      const datos = await respuesta.json();
      setStats2(datos);

    } catch (error) {
      console.error('Error al obtener estadísticas:', error);
    }
  }
  const obtenerEstadisticas_redis = async () => {
    try {
      const respuesta = await fetch('http://localhost:8010/container_redis');
      console.log(respuesta)
      const datos = await respuesta.json();
      setStats3(datos);

    } catch (error) {
      console.error('Error al obtener estadísticas:', error);
    }
  }

  const obtenerEstadisticas_load_balancer = async () => {
    try {
      const respuesta = await fetch('http://localhost:8010/container_ngnix');
      console.log(respuesta)
      const datos = await respuesta.json();
      setStats4(datos);

    } catch (error) {
      console.error('Error al obtener estadísticas:', error);
    }
  }

  const IniciarContenedor = async (contenedor) => {
    try {
      const respuesta = await fetch('http://localhost:8010/container_start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ contenedor: contenedor })
      });
      const datos = await respuesta.json();
      if (datos.status === 400){
        alert("El contenedor se inicio correctamente")
      }else{
        alert("El contenedor ya esta iniciado")
      }
     
      
    } catch (error) {
      alert("Error al iniciar el contenedor")
    }
  }


  useEffect(() => {
    const intervalo = setInterval(() => {
      obtenerEstadisticas_selenium();
      obtenerEstadisticas_playwright();
      obtenerEstadisticas_redis();
      obtenerEstadisticas_load_balancer();
      console.log("Obteniendo estadisticas")
    }, 10000);
    return () => clearInterval(intervalo);
  }, []);
  return (
    <>
      <div className="container">
        <div className="content">
          <h1>DashBoard Web</h1>
          <h2>Estadisticas del Contenedor: Selenium</h2>
          {stats_selenium ? (
            <div className="dash">

              <div className="card">
                <p className="heading">Almacenamiento</p>
                <p>Memory Out: {stats_selenium.almacenamiento.memory_out} MB <br /> Memory In: {stats_selenium.almacenamiento.memory_in} KB</p>
              </div>
              <div className="card">
                <p className="heading">CPU</p>
                <p>Porcentaje: {stats_selenium.cpu.porcentaje}%</p>
              </div>
              <div className="card">
                <p className="heading">RAM</p>
                <p>limite: {stats_selenium.ram.limite} MB
                  <br /> Porcentaje: {stats_selenium.ram.porcentaje}%
                  <br /> Uso: {stats_selenium.ram.uso} MB
                </p>
              </div>
              <div className="card">
                <p className="heading">RED</p>
                <p>Red IN: {stats_selenium.red.red_in} KB
                  <br /> Red OUT: {stats_selenium.red.red_out}KB

                </p>
              </div>
            </div>

          ) : (
            <div className="loading-wave">
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
            </div>
          )}
          <div className="card2">
          <button className="btn" onClick={() => IniciarContenedor("selenium")}> Inicar Contenedor 
          </button>
          <button className="btn" onClick={() => ReiniciarContenedor("selenium")}> Reiniciar Contenedor 
          </button>
          <button className="btn" onClick={() => ApagarContenedor("selenium")}> Apagar Contenedor 
          </button>
          </div>
          <h2>Estadisticas del Contenedor: Playwright</h2>
          {stats_playwright ? (
            <div className="dash">

              <div className="card">
                <p className="heading">Almacenamiento</p>
                <p>Memory Out: {stats_playwright.almacenamiento.memory_out} MB <br /> Memory In: {stats_playwright.almacenamiento.memory_in} KB</p>
              </div>
              <div className="card">
                <p className="heading">CPU</p>
                <p>Porcentaje: {stats_playwright.cpu.porcentaje}%</p>
              </div>
              <div className="card">
                <p className="heading">RAM</p>
                <p>limite: {stats_playwright.ram.limite} MB
                  <br /> Porcentaje: {stats_playwright.ram.porcentaje}%
                  <br /> Uso: {stats_playwright.ram.uso} MB
                </p>
              </div>
              <div className="card">
                <p className="heading">RED</p>
                <p>Red IN: {stats_playwright.red.red_in} KB
                  <br /> Red OUT: {stats_playwright.red.red_out}KB

                </p>
              </div>
            </div>

          ) : (
            <div className="loading-wave">
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
            </div>
          )}
          <div className="card2">
          <button className="btn"> Inicar Contenedor
          </button>
          <button className="btn"> Reiniciar Contenedor
          </button>
          <button className="btn"> Apagar Contenedor
          </button>
          </div>

          <h2>Estadisticas del Contenedor: Redis</h2>
          {stats_redis ? (
            <div className="dash">

              <div className="card">
                <p className="heading">Almacenamiento</p>
                <p>Memory Out: {stats_redis.almacenamiento.memory_out} MB <br /> Memory In: {stats_redis.almacenamiento.memory_in} KB</p>
              </div>
              <div className="card">
                <p className="heading">CPU</p>
                <p>Porcentaje: {stats_redis.cpu.porcentaje}%</p>
              </div>
              <div className="card">
                <p className="heading">RAM</p>
                <p>limite: {stats_redis.ram.limite} MB
                  <br /> Porcentaje: {stats_redis.ram.porcentaje}%
                  <br /> Uso: {stats_redis.ram.uso} MB
                </p>
              </div>
              <div className="card">
                <p className="heading">RED</p>
                <p>Red IN: {stats_redis.red.red_in} KB
                  <br /> Red OUT: {stats_redis.red.red_out}KB

                </p>
              </div>
            </div>

          ) : (
            <div className="loading-wave">
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
            </div>
          )}
          <div className="card2">
          <button className="btn"> Inicar Contenedor
          </button>
          <button className="btn"> Reiniciar Contenedor
          </button>
          <button className="btn"> Apagar Contenedor
          </button>
          </div>

          <h2>Estadisticas del Contenedor: Load Balancer</h2>
          {stats_load_balancer ? (
            <div className="dash">

              <div className="card">
                <p className="heading">Almacenamiento</p>
                <p>Memory Out: {stats_load_balancer.almacenamiento.memory_out} MB <br /> Memory In: {stats_load_balancer.almacenamiento.memory_in} KB</p>
              </div>
              <div className="card">
                <p className="heading">CPU</p>
                <p>Porcentaje: {stats_load_balancer.cpu.porcentaje}%</p>
              </div>
              <div className="card">
                <p className="heading">RAM</p>
                <p>limite: {stats_load_balancer.ram.limite} MB
                  <br /> Porcentaje: {stats_load_balancer.ram.porcentaje}%
                  <br /> Uso: {stats_load_balancer.ram.uso} MB
                </p>
              </div>
              <div className="card">
                <p className="heading">RED</p>
                <p>Red IN: {stats_load_balancer.red.red_in} KB
                  <br /> Red OUT: {stats_load_balancer.red.red_out}KB

                </p>
              </div>
            </div>

          ) : (
            <div className="loading-wave">
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
              <div className="loading-bar"></div>
            </div>
          )}
          <div className="card2">
          <button className="btn"> Inicar Contenedor
          </button>
          <button className="btn"> Reiniciar Contenedor
          </button>
          <button className="btn"> Apagar Contenedor
          </button>
          </div>
          <div><br/></div>

        </div>
      </div>
    </>

  );
};

export default App;