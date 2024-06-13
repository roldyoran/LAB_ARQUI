# LIBRERIAS
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time

# MODULOS
import RPi.GPIO as GPIO
import gpio_setup as led
import porton_setup as porton
import banda_setup as banda


# MODULO TEST MAGICK
# from unittest.mock import MagicMock
# import mock_gpio_setup as led
# GPIO = MagicMock()



#Colocar modo de los pines aqui antes de los setups
GPIO.setmode(GPIO.BOARD)

NOCHE = 15
LASER = 27
ALARMA = 7
GPIO.setup(NOCHE, GPIO.IN)
GPIO.setup(LASER, GPIO.IN)
GPIO.setup(ALARMA, GPIO.OUT)


# Inicializa la configuración de los pines
led.setup()
porton.setup()
banda.setup()



# Define los pines GPIO que vas a usar
PIN_1 = 31  # Puedes cambiar estos valores segÃºn tu configuraciÃ³n
PIN_2 = 32

LED_PINS = [11, 13, 19, 18]  # Pins fÃ­sicos 11, 13, 15 y 18 corresponden a GPIO17, GPIO27, GPIO22 y GPIO24 respectivamente
binario = [	[GPIO.LOW,  GPIO.LOW,   GPIO.LOW,   GPIO.LOW],
			[GPIO.LOW,  GPIO.LOW,   GPIO.LOW,   GPIO.HIGH],
			[GPIO.LOW,  GPIO.LOW,   GPIO.HIGH,  GPIO.LOW],
			[GPIO.LOW,  GPIO.LOW,   GPIO.HIGH,  GPIO.HIGH],
			[GPIO.LOW,  GPIO.HIGH,  GPIO.LOW,   GPIO.LOW],
			[GPIO.LOW,  GPIO.HIGH,  GPIO.LOW,   GPIO.HIGH],
			[GPIO.LOW,  GPIO.HIGH,  GPIO.HIGH,  GPIO.LOW],
			[GPIO.LOW,  GPIO.HIGH,  GPIO.HIGH,  GPIO.HIGH],
			[GPIO.HIGH, GPIO.LOW,   GPIO.LOW,   GPIO.LOW],
			[GPIO.HIGH, GPIO.LOW,   GPIO.LOW,   GPIO.HIGH],
]

# Contadores de personas
counter = 0
ingresos = 0
# Variables para guardar el estado anterior de los pines
prev_state_pin1 = False
prev_state_pin2 = False

# Configurar los pines GPIO como entradas
GPIO.setup(PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_PINS[0], GPIO.OUT)
GPIO.setup(LED_PINS[1], GPIO.OUT)
GPIO.setup(LED_PINS[2], GPIO.OUT)
GPIO.setup(LED_PINS[3], GPIO.OUT)




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

banda_setup = {'banda': False}

alarma_setup = {'alarma': False}


# BANDA TRANSPORADORA (APAGAR Y ENCENDER)
@app.route('/control_banda_transportadora', methods=['POST'])
def control_banda_transportadora():
    global banda_setup
    data = request.get_json()

    if 'encendido' in data:
        banda_setup['banda'] = data['encendido']
        if banda_setup['banda']:
            banda.encender_banda()
        else:
            banda.apagar_banda()
    # print(porton)
    return jsonify(banda_setup)

# APAGADO DE PINES (EMERGENCIA)
@app.route('/apagar_pines', methods=['POST'])
def apagar_pines():
    # Aqui se apagan los puertos
    porton.desactivar_todo()
    led.apagar_todo()
    return jsonify({"message": "Pines apagados con éxito"})


# PORTON (PUERTA TRASERA)
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

# LUCES LED PARA EL FRONT 
@app.route('/estado_luces', methods=['GET'])
def get_luces_state():
    # led.activar_leds()
    return jsonify(estado_luces)

# APAGADO Y ENCENDIDO DE LAS LUCES
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


# APAGADO Y ENCENDIDO DE LA ALARMA
@app.route('/alarma_estado', methods=['GET'])
def alarma_estado():
    global alarma_setup
    return jsonify(alarma_setup)

# Numero de Clientes
@app.route('/numero_clientes', methods=['GET'])
def get_numero():
    global counter
    return jsonify({'numero': counter})



"""HILO"""
def display_siete_segmentos(numero):
    global LED_PINS
    GPIO.setup(LED_PINS[0], numero[0])
    GPIO.setup(LED_PINS[1], numero[1])
    GPIO.setup(LED_PINS[2], numero[2])
    GPIO.setup(LED_PINS[3], numero[3])
    time.sleep(4)


# Hilo para monitorear la fotoresistencia
def monitor_fotoresistencia():
    global alarma_setup, counter, ingresos,prev_state_pin1, prev_state_pin2
    while True:
        """ALARMA"""
        if GPIO.input(NOCHE):
            # SI la fotoresistencia no detecta la luz del laser envia un 1
            set_lights('exterior')
            # significa que la luz del laser no llego, hay un intruso y se enciende la alarma (buzzer)
            if GPIO.input(LASER):
               #  Aqui se enciende la alarma, por el momento solo es un print
                print("ALARMA ENCENDIDA, SE DETECTO UN INSTRUSO")  
                alarma_setup['alarma'] = True
                GPIO.setup(ALARMA, GPIO.HIGH)
                time.sleep(10)
                GPIO.setup(ALARMA, GPIO.LOW)
                alarma_setup['alarma'] = False
        """SENSORES ENTRADA"""
        # Leer el estado actual de los pines
        state_pin1 = GPIO.input(PIN_1)
        state_pin2 = GPIO.input(PIN_2)

        # Detectar el cambio de estado del pin 1
        if state_pin1 and not prev_state_pin1:
            # Si pin 1 estÃ¡ activado y pin 2 no lo estaba
            if prev_state_pin2:
                counter -= 1
                print(f"Saliendo {counter}")
                if counter <= 9 and counter >= 0:
                    display_siete_segmentos(binario[counter])
        
        # Detectar el cambio de estado del pin 2
        if state_pin2 and not prev_state_pin2:
            # Si pin 2 estÃ¡ activado y pin 1 no lo estaba
            if prev_state_pin1:
                counter += 1
                print(f"Entrando {counter}")
                ingresos += 1
                if counter <= 9 and counter >= 0:
                    display_siete_segmentos(binario[counter])


        # Actualizar el estado anterior de los pines
        prev_state_pin1 = state_pin1
        prev_state_pin2 = state_pin2
        time.sleep(0.05)  # Ajusta el tiempo de espera según sea necesario

# Iniciar el hilo de la fotoresistencia
threading.Thread(target=monitor_fotoresistencia, daemon=True).start()











# INICIANDO EL PROGRAMA
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
