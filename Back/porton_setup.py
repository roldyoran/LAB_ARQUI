import RPi.GPIO as GPIO
import time

SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500
Servo = 23



def map(value, inMin, inMax, outMin, outMax):
    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin

def setup():
    global p
    GPIO.setmode(GPIO.BOARD)       
    GPIO.setup(Servo, GPIO.OUT)  
    GPIO.output(Servo, GPIO.LOW) 
    p = GPIO.PWM(Servo, 50)     
    p.start(0)                    

def setAngle(angle):      
    global p
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)

# def loop():
#     while True:
#         # ACTIVAR
#         for i in range(0, 181, 5):   
#             setAngle(i)    
#             time.sleep(0.002)
#         time.sleep(1)
#         # DESACTIVAR
#         for i in range(180, -1, -5): 
#             setAngle(i)
#             time.sleep(0.001)
        # time.sleep(1)

def abrir_porton():
    global p
    # ACTIVAR
    print("abriendo")
    for i in range(0, 181, 5):   
        setAngle(i)    
        time.sleep(0.002)
    time.sleep(1)

def cerrar_porton():
    global p
    # DESACTIVAR
    print("cerrando")
    p.start()
    # for i in range(180, -1, -5): 
    #     setAngle(i)
    #     time.sleep(0.001)
    # time.sleep(1) 

def desactivar_todo():
    global p
    setAngle(0)
    time.sleep(1)
    p.stop()