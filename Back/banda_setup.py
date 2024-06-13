import RPi.GPIO as GPIO
import time


BANDA_TRANSPORTADORA = 22
GPIO.setmode(GPIO.BOARD)

def setup():
    global BANDA_TRANSPORTADORA
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BANDA_TRANSPORTADORA, GPIO.OUT)  

def encender_banda():
    global BANDA_TRANSPORTADORA
    GPIO.setup(BANDA_TRANSPORTADORA, GPIO.HIGH)
    time.sleep(1)

def apagar_banda():
    global BANDA_TRANSPORTADORA
    GPIO.setup(BANDA_TRANSPORTADORA, GPIO.LOW)
    time.sleep(1)

