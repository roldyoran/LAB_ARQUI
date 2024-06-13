import RPi.GPIO as GPIO
import time

# Configurar el modo de los pines GPIO
GPIO.setmode(GPIO.BOARD)  # Usa la numeraciÃ³n de pines BCM

# Define los pines GPIO que vas a usar
PIN_1 = 8  # Puedes cambiar estos valores segÃºn tu configuraciÃ³n
PIN_2 = 10

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

def setup():
    global PIN_1, PIN_2, LED_PINS
    # Configurar los pines GPIO como entradas
    GPIO.setup(PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(LED_PINS[0], GPIO.OUT)
    GPIO.setup(LED_PINS[1], GPIO.OUT)
    GPIO.setup(LED_PINS[2], GPIO.OUT)
    GPIO.setup(LED_PINS[3], GPIO.OUT)



def display_siete_segmentos(numero):
    global LED_PINS
    GPIO.setup(LED_PINS[0], numero[0])
    GPIO.setup(LED_PINS[1], numero[1])
    GPIO.setup(LED_PINS[2], numero[2])
    GPIO.setup(LED_PINS[3], numero[3])
    time.sleep(4)



try:
    while True:
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

        # PequeÃ±a pausa para evitar consumir demasiados recursos
        time.sleep(0.04)

except KeyboardInterrupt:
    # Limpiar la configuraciÃ³n de los pines GPIO al terminar
    GPIO.cleanup()

