import RPi.GPIO as GPIO
import board
import time
GPIO.setmode(GPIO.BCM)
BUTTON = 18
GPIO.setup(BUTTON, GPIO.IN)

while True:
    if GPIO.input(BUTTON) == GPIO.LOW:
        print("I got no plans.")
    else:
        while GPIO.input(BUTTON) == GPIO.HIGH:
            pass
        print("I got real big plans.")
    time.sleep(0.1)

