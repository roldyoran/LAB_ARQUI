import React, { useState, useEffect } from 'react';
import './Banda.css'; // Asegúrate de importar el archivo CSS
import { API_URL } from '../config';

const PostButton = () => {
  const [bandaActiva, setBandaActiva] = useState(false);

  const handleClick = async () => {
    try {
      const response = await fetch(`${API_URL}/control_banda_transportadora`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ encendido: !bandaActiva }), // Enviar el estado inverso
      });

      const result = await response.json();
      setBandaActiva(result.banda); // Actualizar el estado según la respuesta del servidor
      alert(result.message);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="banda-container">
      <button 
        onClick={handleClick} 
        className={`button-banda ${bandaActiva ? 'active' : 'deactive'}`}
      >
        {bandaActiva ? 'APAGAR BANDA' : 'ACTIVAR BANDA'}
      </button>
      <p className="banda-status">
        {bandaActiva ? 'BANDA EN MOVIMIENTO' : 'BANDA APAGADA'}
      </p>
    </div>
  );
};

export default PostButton;
