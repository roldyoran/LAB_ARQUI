import React from 'react';
import './ApagarTodo.css'; // Asegúrate de importar el archivo CSS
import { API_URL } from '../config';

const PostButton = () => {
  const handleClick = async () => {
    try {
      const response = await fetch(`${API_URL}/apagar_pines`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ key: 'value' }), // Reemplaza esto con los datos que deseas enviar
      });

      const result = await response.json();
    //   console.log('Success:', result);
    alert(result.message);
    } catch (error) {
      console.error('Error:', error);
    }
  };

 
  return (
    <button 
      onClick={handleClick} 
      className="button"
    >
      APAGAR GPIO (PINES)
    </button>
  );
};

export default PostButton;