import RPi.GPIO as GPIO

# Puertos
DECODER1 = 11
DECODER2 = 12
DECODER3 = 13

FOTORESISTENCIA_EXTERIOR = 15

# Inicializar GPIO
GPIO.setmode(GPIO.BOARD)

def activar_leds():
    # Seleccionar salida
    GPIO.setup(DECODER1, GPIO.OUT)
    GPIO.setup(DECODER2, GPIO.OUT)
    GPIO.setup(DECODER3, GPIO.OUT)

def activar_fotoresistencia():
    GPIO.setup(FOTORESISTENCIA_EXTERIOR, GPIO.IN)

def desactivar_leds():
    # Desactiva los pines de las leds
    GPIO.setup(DECODER1, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(DECODER2, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(DECODER3, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

# Función para configurar los LEDs
def set_leds(state):
    GPIO.output(DECODER1, state[0])
    GPIO.output(DECODER2, state[1])
    GPIO.output(DECODER3, state[2])