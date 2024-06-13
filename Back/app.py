# LIBRERIAS
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time

# MODULOS
import RPi.GPIO as GPIO
import gpio_setup as led
import porton_setup as porton


# MODULO TEST MAGICK
# from unittest.mock import MagicMock
# import mock_gpio_setup as led
# GPIO = MagicMock()



#Colocar modo de los pines aqui antes de los setups
GPIO.setmode(GPIO.BOARD)
FOTO_RESISTENCIA = 15
GPIO.setup(FOTO_RESISTENCIA, GPIO.IN)

# Inicializa la configuración de los pines
led.setup()
# porton.setup()


app = Flask(__name__)
CORS(app)

# Estado inicial de las luces en cada habitación
estado_luces = {
    'recepcion': False,
    'conferencias': False,
    'trabajo': False,
    'administrativa': False,
    'carga_descarga': False,
    'cafeteria': False,
    'bano': False,
    'exterior': False
}

# Diccionario de código binario para las luces
codigo_binario_luces = {
    'recepcion':        [ GPIO.LOW,  GPIO.LOW,  GPIO.LOW  ],
    'conferencias':     [ GPIO.LOW,  GPIO.LOW,  GPIO.HIGH ],
    'trabajo':          [ GPIO.LOW,  GPIO.HIGH, GPIO.LOW  ],
    'administrativa':   [ GPIO.LOW,  GPIO.HIGH, GPIO.HIGH ],
    'carga_descarga':   [ GPIO.HIGH, GPIO.LOW,  GPIO.LOW  ],
    'cafeteria':        [ GPIO.HIGH, GPIO.LOW,  GPIO.HIGH ],
    'bano':             [ GPIO.HIGH, GPIO.HIGH, GPIO.LOW  ],
    'exterior':         [ GPIO.HIGH, GPIO.HIGH, GPIO.HIGH ]
}

porton_setup = {'porton': False}



@app.route('/estado_luces', methods=['GET'])
def get_luces_state():
    # led.activar_leds()
    return jsonify(estado_luces)


@app.route('/apagar_pines', methods=['POST'])
def apagar_pines():
    # Aqui se apagan los puertos
    porton.desactivar_todo()
    led.apagar_todo()
    return jsonify({"message": "Pines apagados con éxito"})

@app.route('/control_porton', methods=['POST'])
def control_porton():
    global porton_setup
    data = request.get_json()
    # print(data)
    if 'encendido' in data:
        porton_setup['porton'] = data['encendido']
        if porton_setup['porton']:
            porton.abrir_porton()
        else:
            porton.cerrar_porton()
    # print(porton)
    return jsonify(porton_setup)


"""LUCES LEDS HABITACIONES"""
# Función para establecer el estado de los LEDs según el modo
def set_lights(mode):
    if mode in codigo_binario_luces:
        led.set_leds(codigo_binario_luces[mode])
    else:
        print("Modo no reconocido")

@app.route('/control_luz', methods=['POST'])
def control_luz():
    global estado_luces
    data = request.get_json()
    print(data)
    if 'habitacion' in data and 'encendido' in data:
        habitacion = data['habitacion']
        for cuarto in estado_luces:
            estado_luces[cuarto] = False
        estado_luces[habitacion] = data['encendido']
        if data['encendido'] and habitacion != None:
            set_lights(habitacion)
            time.sleep(1)
        else:
            led.set_leds([GPIO.LOW, GPIO.LOW, GPIO.LOW])
            time.sleep(1)
    return jsonify(estado_luces)



# Hilo para monitorear la fotoresistencia
def monitor_fotoresistencia():
    while True:
        if GPIO.input(FOTO_RESISTENCIA):
            set_lights('exterior')
        time.sleep(2)  # Ajusta el tiempo de espera según sea necesario

# Iniciar el hilo de la fotoresistencia
threading.Thread(target=monitor_fotoresistencia, daemon=True).start()


# INICIANDO EL PROGRAMA
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
