import time
from gpiozero import LED
from gpiozero import Button

led1 = LED(14)
button = Button(17)

try:
    while True:
        led1.on()
        print(button.is_active)
        time.sleep(0.1)
        led1.off()
        time.sleep(0.1)
except KeyboardInterrupt:
    led1.close()
    led2.close()