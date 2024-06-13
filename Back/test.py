import RPi.GPIO as GPIO
import time




GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)  # LED VERDE 
# GPIO.setup(24, GPIO.OUT)  # LED ROJA 

# green_led = GPIO.HIGH
# red_led = GPIO.PWM(24, 100)

# green_led.start(0)  # LED VERDE
# red_led.start(100)  # LED ROJA 

try:
    GPIO.setup(25, GPIO.HIGH)
    # red_led.ChangeDutyCycle(0)
    time.sleep(10)

    
    # green_led.ChangeDutyCycle(0)
    # red_led.ChangeDutyCycle(100)

    time.sleep(5)
    GPIO.setup(25, GPIO.LOW)
    time.sleep(2)
    GPIO.cleanup()

except KeyboardInterrupt:
    # green_led.stop()
    # red_led.stop()
    GPIO.cleanup()