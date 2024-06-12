import React, { useState, useEffect } from 'react';
import { API_URL } from './config';
import './App.css';

function App() {
  const [luces, setLuces] = useState({
    recepcion: false,
    conferencias: false,
    trabajo: false,
    administrativa: false,
    carga_descarga: false,
    cafeteria: false,
    bano: false,
    exterior: false,
  });

  useEffect(() => {
    fetch(`${API_URL}/estado_luces`)
      .then(response => response.json())
      .then(data => {
        setLuces(data);
      })
      .catch(error => {
        console.error('Hubo un error!', error);
      });
  }, []);

  const toggleLuz = (habitacion) => {
    fetch(`${API_URL}/control_luz`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        habitacion: habitacion,
        encendido: !luces[habitacion]
      })
    })
    .then(response => response.json())
    .then(data => {
      setLuces(data);
    })
    .catch(error => {
      console.error('Hubo un error!', error);
    });
  };




  
  const habitaciones = [
    { id: 'recepcion', nombre: 'Recepción' },
    { id: 'conferencias', nombre: 'Área de Conferencias' },
    { id: 'trabajo', nombre: 'Área de Trabajo' },
    { id: 'administrativa', nombre: 'Área Administrativa' },
    { id: 'carga_descarga', nombre: 'Área de Carga y Descarga' },
    { id: 'cafeteria', nombre: 'Cafetería' },
    { id: 'bano', nombre: 'Baño' },
    { id: 'exterior', nombre: 'Exterior' },
  ];

  return (
    <div className="App">
      <h1>Control de Luces</h1>
      <div className="planta">
        {habitaciones.map(habitacion => (
          <div key={habitacion.id} className="habitacion" 
          onClick={() => toggleLuz(habitacion.id)}>
            <div 
              className={`foco ${luces[habitacion.id] ? 'encendido' : 'apagado'}`}
            ></div>
            <p>{habitacion.nombre}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
