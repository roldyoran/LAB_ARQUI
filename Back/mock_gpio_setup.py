from unittest.mock import MagicMock

GPIO = MagicMock()

# Puertos
DECODER1 = 11
DECODER2 = 12
DECODER3 = 13

FOTORESISTENCIA_EXTERIOR = 15

# Inicializar GPIO
GPIO.setmode(GPIO.BOARD)

# Función para configurar los pines como salidas
def setup():
    GPIO.setmode(GPIO.BOARD)  # o GPIO.BOARD, según tu configuración
    GPIO.setup(DECODER1, GPIO.OUT)
    GPIO.setup(DECODER2, GPIO.OUT)
    GPIO.setup(DECODER3, GPIO.OUT)

def desactivar_leds():
    # Desactiva los pines de las leds
    GPIO.setup(DECODER1, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(DECODER2, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(DECODER3, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

def apagar_todo():
    GPIO.cleanup()

# Función para configurar los LEDs
def set_leds(state):
    GPIO.output(DECODER1, state[0])
    GPIO.output(DECODER2, state[1])
    GPIO.output(DECODER3, state[2])

    # GPIO.cleanup()