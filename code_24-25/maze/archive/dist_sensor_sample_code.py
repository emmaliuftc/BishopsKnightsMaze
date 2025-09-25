# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import busio
import adafruit_vl53l0x
import digitalio
import board


power_pin1 = digitalio.DigitalInOut(board.D15)
power_pin2 = digitalio.DigitalInOut(board.D18)
power_pin3 = digitalio.DigitalInOut(board.D23)
power_pin4 = digitalio.DigitalInOut(board.D24)

def on(x):
    x.switch_to_output(value=True)

def off(x):
    x.switch_to_output(value=False)
    

off(power_pin1)
off(power_pin2)
off(power_pin3)
on(power_pin4)

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)


# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
# vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

# Main loop will read the range and print it every second.
for i in range(5):
    print("Range: {0}mm".format(vl53.range))
    time.sleep(1.0)
    
off(power_pin4)

on(power_pin3)
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

for i in range(5):
    print("Range: {0}mm".format(vl53.range))
    time.sleep(1.0)
    



