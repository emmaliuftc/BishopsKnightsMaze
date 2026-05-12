import time
import busio
import math
from statistics import mode
import board
import adafruit_tca9548a
import adafruit_vl6180x
import adafruit_vl53l0x
import adafruit_tcs34725
import math
from adafruit_bno08x.i2c import BNO08X_I2C


i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # 100000 ?
tca = adafruit_tca9548a.TCA9548A(i2c)
color = adafruit_tcs34725.TCS34725(tca[5])

bl_clear_rng = [0,10]
s_clear_rng = [50,1000]
special_clear_rng = [41,90]
br_clear_rng = [20,40]
r_clear_rng = [20,40]
w_clear_rng = [75,90]
bu_clear_rng = [20,40]

detected_colors = []
total_clear = 0
total_red = 0
total_lux = 0

for i in range(10):
    
    clear_reading = color.color_raw[3]
    red_reading = color.color_raw[0]
    lux_reading = color.lux
    print(clear_reading)
    print(red_reading)
    print(lux_reading)

    total_clear += clear_reading
    total_red += red_reading
    total_lux += lux_reading

clear_average = total_clear/10
red_average = total_red/10
lux_average = total_lux/10

# differentiate silver and white
if 82 < clear_average < 90 and lux_average > 2500:
    detected_colors.append('w')
elif 75 < clear_average < 82 and lux_average > 2500:
    detected_colors.append('si')

# differentiate red and blue
if 22 < clear_average < 32 and 14 < red_average < 24:
    detected_colors.append('r')
elif 22 < clear_average < 32 and lux_average < 7:
    detected_colors.append('bu')

if 0 < clear_average < 10:
    detected_colors.append('bl')

# check for max color
if len(detected_colors)==0:
    color = 'none'
else:
    color = mode(detected_colors)
print(f"return value for get_color: {color}")
print(color)
