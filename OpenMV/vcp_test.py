# Untitled - By: student - Mon May 4 2026

import time
import pyb

vcp = pyb.USB_VCP()
led = pyb.LED(3)

while(True):
    led.toggle()
    vcp.write("OpenMV chillin\n")

    time.sleep_ms(500)
