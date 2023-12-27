import React, { useState, useEffect } from 'react';
import Swal from 'sweetalert2';
import './App.css';
import StatsComponent from './cards';
import LoadingWaveComponent from './loadingWave';
const App = () => {
  const [error, setError] = useState(null);
  const [stats_contenedores, setStatsContenedores] = useState({
    selenium: null,
    playwright: null,
    redis: null,
    nginx: null,
  });
  const obtenerEstadisticas = async (contenedor) => {
    try {
      const respuesta = await fetch(`http://localhost:8010/container_${contenedor}`);
      const datos = await respuesta.json();
      setStatsContenedores((prevStats) => ({
        ...prevStats,
        [contenedor]: datos,
      }));
    } catch (error) {
      setError(error);
      console.error(`Error al obtener estadísticas para ${contenedor}:`, error);
    }
  };

  const controlarContenedor = async (accion, contenedor) => {
    try {
      const respuesta = await fetch(`http://localhost:8010/container_${accion}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ contenedor: contenedor }),
      });
      const datos = await respuesta.json();

      if (datos.status === 200) {
        Swal.fire({
          icon: 'error',
          title: `Contenedor No ${accion}`,
          text: `El contenedor ya se encuentra ${accion === 'stop' ? 'detenido' : 'iniciado'}`,
          confirmButtonText: 'Aceptar',
        });
      } else {
        Swal.fire({
          icon: 'success',
          title: `Contenedor ${accion === 'restart' ? 'reiniciado' : accion}`,
          text: `El contenedor se ${accion === 'restart' ? 'reinicio' : accion} correctamente`,
          confirmButtonText: 'Aceptar',
          didClose: () => {
            window.location.reload();
          },
        });
      }
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: `Contenedor No ${accion}`,
        text: `Error al ${accion === 'stop' ? 'detener' : accion} el contenedor`,
        confirmButtonText: 'Aceptar',
        didClose: () => {
          window.location.reload();
        },
      });
    }
  };

  useEffect(() => {
    const intervalo = setInterval(() => {
      obtenerEstadisticas('selenium');
      obtenerEstadisticas('playwright');
      obtenerEstadisticas('redis');
      obtenerEstadisticas('nginx');
      console.log('Obteniendo estadisticas');
    }, 5000);

    return () => clearInterval(intervalo);
  }, []);

  const ContainerControlComponent = (props) => (
    <div className="card2">
      <button className="btn" onClick={() => controlarContenedor('start', props.contenedor)}>
        Iniciar Contenedor
      </button>
      <button className="btn" onClick={() => controlarContenedor('restart', props.contenedor)}>
        Reiniciar Contenedor
      </button>
      <button className="btn" onClick={() => controlarContenedor('stop', props.contenedor)}>
        Apagar Contenedor
      </button>
    </div>
  );
  
  const ordenarPorUsoRAM = () => {
    const contenedoresOrdenados = Object.keys(stats_contenedores).sort(
      (a, b) =>
        stats_contenedores[b]?.ram.uso - stats_contenedores[a]?.ram.uso || 0
    );

    setStatsContenedores((prevStats) => {
      const nuevoOrden = {};
      contenedoresOrdenados.forEach((contenedor) => {
        nuevoOrden[contenedor] = prevStats[contenedor];
      });
      return nuevoOrden;
    });
  };

  const ordenarPorUsoCPU = () => {
    const contenedoresOrdenados = Object.keys(stats_contenedores).sort(
      (a, b) =>
        stats_contenedores[b]?.cpu.porcentaje - stats_contenedores[a]?.cpu.porcentaje || 0
    );

    setStatsContenedores((prevStats) => {
      const nuevoOrden = {};
      contenedoresOrdenados.forEach((contenedor) => {
        nuevoOrden[contenedor] = prevStats[contenedor];
      });
      return nuevoOrden;
    });
  };
  const ordenarPorUsoAlmacenamiento = () => {
    const contenedoresOrdenados = Object.keys(stats_contenedores).sort(
      (a, b) =>
        stats_contenedores[b]?.almacenamiento.memory_in - stats_contenedores[a]?.almacenamiento.memory_in || 0
    );
  
    setStatsContenedores((prevStats) => {
      const nuevoOrden = {};
      contenedoresOrdenados.forEach((contenedor) => {
        nuevoOrden[contenedor] = prevStats[contenedor];
      });
      return nuevoOrden;
    });
  };
  const ordenarPorUsoRed = () => {
    const contenedoresOrdenados = Object.keys(stats_contenedores).sort(
      (a, b) =>
        stats_contenedores[b]?.red.red_in - stats_contenedores[a]?.red.red_in || 0
    );
  
    setStatsContenedores((prevStats) => {
      const nuevoOrden = {};
      contenedoresOrdenados.forEach((contenedor) => {
        nuevoOrden[contenedor] = prevStats[contenedor];
      });
      return nuevoOrden;
    });
  };

  return (
    <>
      <div className="container">
        <div className="content">
          <h1>DashBoard Web</h1>
          <div>

            <button className='btn' onClick={ordenarPorUsoRAM}>Ordenar por uso de RAM</button>
            <button className='btn' onClick={ ordenarPorUsoCPU}>Ordenar por uso de CPU</button>
            <button className='btn' onClick={ordenarPorUsoAlmacenamiento}>Ordenar por uso de Almacenamiento</button>
            <button className='btn' onClick={ordenarPorUsoRed}>Ordenar por uso de RED</button>
          </div>


          {Object.keys(stats_contenedores).map((contenedor) => (
            <React.Fragment key={contenedor}>
              {stats_contenedores[contenedor] ? (
                <StatsComponent titulo={contenedor} stats={stats_contenedores[contenedor]} />
              ) : (
                <LoadingWaveComponent />
              )}
              <ContainerControlComponent contenedor={contenedor} />

            </React.Fragment>
          ))}
        </div>

      </div>
    </>

  );
};

export default App;