import React, { useState } from 'react';
import './Porton.css'; // Asegúrate de importar el archivo CSS
import { API_URL } from '../config';

const PostButton = () => {
  const [porton, setPorton] = useState(false);

  const togglePorton = () => {
    fetch(`${API_URL}/control_porton`, {  // Suponiendo que la URL es /control_porton
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        encendido: !porton
      })
    })
    .then(response => response.json())
    .then(data => {
      setPorton(!porton);
    })
    .catch(error => {
      console.error('Hubo un error!', error);
    });
  };

  return (
    <button 
      onClick={togglePorton} 
      className={`porton-button ${porton ? 'porton-button-on' : 'porton-button-off'}`}
    >
      {porton ? 'CERRAR PORTÓN' : 'ABRIR PORTÓN'}
    </button>
  );
};

export default PostButton;
