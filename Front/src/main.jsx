import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import ApagarTodo from './componente/ApagarTodo.jsx'
import ControlPorton from './componente/Porton.jsx'
import Alarma from './componente/Alarma.jsx'
import Banda from './componente/Banda.jsx'
import N_clientes from './componente/N_clientes.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <div className="main-container">
      <ControlPorton />
      <ApagarTodo />
      <Banda />
      <App />
      <N_clientes />
      <Alarma />
    </div>
  </React.StrictMode>,
)
