import React from 'react';

const StatsComponent = ({ titulo ,stats }) => {
  console.log(titulo)
  return (
    <>
      <h2>Estadisticas del Contenedor: {titulo}</h2>
      <div className="dash">
        <div className="card">
          <p className="heading">Almacenamiento</p>
          <p>
            Memory Out: {stats.almacenamiento.memory_out} MB <br />
            Memory In: {stats.almacenamiento.memory_in} KB
          </p>
        </div>
        <div className="card">
          <p className="heading">CPU</p>
          <p>Porcentaje: {stats.cpu.porcentaje}%</p>
        </div>
        <div className="card">
          <p className="heading">RAM</p>
          <p>
            Limite: {stats.ram.limite} MB <br />
            Porcentaje: {stats.ram.porcentaje}% <br />
            Uso: {stats.ram.uso} MB
          </p>
        </div>
        <div className="card">
          <p className="heading">RED</p>
          <p>
            Red IN: {stats.red.red_in} KB <br />
            Red OUT: {stats.red.red_out} KB
          </p>
        </div>
      </div>
    </>
  );
};

export default StatsComponent;
