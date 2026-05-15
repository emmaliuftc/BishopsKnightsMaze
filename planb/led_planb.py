import time
from gpiozero import LED
from gpiozero import Button

led1 = LED(14)

def flash(sec, times):
    for i in range(times):
        led1.on()
        time.sleep(sec)
        led1.off()
        time.sleep(sec)
flash(1,5)