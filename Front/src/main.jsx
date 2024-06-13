import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import ApagarTodo from './componente/ApagarTodo.jsx'
import ControlPorton from './componente/Porton.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <div className="main-container">
      <ControlPorton />
      <ApagarTodo />
      <App />
    </div>
  </React.StrictMode>,
)
