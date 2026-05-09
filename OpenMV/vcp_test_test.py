# Untitled - By: student - Mon May 4 2026

import sensor
import time
import pyb

leds = [pyb.LED(1), pyb.LED(2), pyb.LED(3)]

while(True):
    for l in leds:
        l.on()
        time.sleep_ms(200)
        l.off()

# sensor.reset()
# sensor.set_pixformat(sensor.RGB565)
# sensor.set_framesize(sensor.QVGA)
# sensor.skip_frames(time=2000)

# vcp = pyb.USB_VCP()
# led = pyb.LED(3)

# while(True):
#     led.toggle()
#     vcp.write("OpenMV chillin\n")

#     time.sleep_ms(500)
