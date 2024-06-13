import React, { useState, useEffect } from 'react';
import './Clientes.css'; // Asegúrate de importar el archivo CSS
import { API_URL } from '../config';

function NumeroComponent() {
  const [numero, setNumero] = useState(null);

  useEffect(() => {
    const fetchNumero = () => {
      fetch(`${API_URL}/numero_clientes`)
        .then(response => response.json())
        .then(data => setNumero(data.numero))
        .catch(error => console.error('Error fetching the number:', error));
    };

    // Llamamos a fetchNumero inicialmente
    fetchNumero();

    // Configuramos un intervalo para llamar fetchNumero cada segundo
    const interval = setInterval(fetchNumero, 1000);

    // Devolvemos una función de limpieza para detener el intervalo cuando el componente se desmonte
    return () => clearInterval(interval);
  }, []); // El array vacío [] asegura que useEffect se ejecute solo una vez al montar el componente

  return (
    <div className="numero-container">
      {numero !== null ? (
        <div className="displayy">
          <h1>{numero}</h1>
          <p>clientes</p>
        </div>
      ) : (
        <div className="displayy">
          <h1>0</h1>
          <p>Clientes</p>
        </div>
      )}
    </div>
  );
}

export default NumeroComponent;
