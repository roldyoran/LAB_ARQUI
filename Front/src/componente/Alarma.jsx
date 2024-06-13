import React, { useState, useEffect } from 'react';
import './Alarma.css'; // Importa el archivo CSS
import { API_URL } from '../config';

const ALARMA = () => {
  const [alarma, setAlarma] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_URL}/alarma_estado`);
        const data = await response.json();
        setAlarma(data.alarma);
      } catch (error) {
        console.error('Error al obtener los datos:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="alarma-container">
      <label className={`alarma-label ${alarma ? 'alarma-on' : 'alarma-off'}`}>
        {alarma ? 'Alarma Encendida' : 'ALARMA Apagada'}
      </label>
    </div>
  );
};

export default ALARMA;
