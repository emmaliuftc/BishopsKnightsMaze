import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pin_num=14
GPIO.setup(pin_num, GPIO.OUT)
GPIO.output(pin_num, GPIO.LOW)


#while True: 
for i in range(6):
    GPIO.output(pin_num, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin_num, GPIO.LOW)
    time.sleep(0.5)
