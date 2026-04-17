import time
from gpiozero import LED
from gpiozero import Button

led1 = LED(14)
led2 = LED(15)
button = Button(18)

try:
    while True:
        led1.on()
        led2.on()
        print(button.is_active)
        time.sleep(0.1)
except KeyboardInterrupt:
    led1.close()
    led2.close()