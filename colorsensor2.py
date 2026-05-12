import math
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
sensor = adafruit_tcs34725.TCS34725(tca[5])

r, g, b = sensor.color_rgb_bytes
l = sensor.lux
print(l)

list_of_color_names = ["Red", "Blue", "Black", "Silver", "White"]
list_of_color_tuples = [(125, 8, 8, 124), (2, 13, 37, 207), (45, 0, 0, 17), (25, 12, 12, 285), (11, 11, 11, 414)]

def closest_color(r,g, b, l=0):
    print(r,g,b,l)
    closest_color_diff = 1000000
    closest_color_name = "Unknown"
    for i in range(len(list_of_color_tuples)):
        red_diff = r - list_of_color_tuples[i][0]
        green_diff = g - list_of_color_tuples[i][1]
        blue_diff = b - list_of_color_tuples[i][2]
        l_diff = l - list_of_color_tuples[i][3]
        diff = math.sqrt((red_diff**2)+(green_diff**2)+(blue_diff**2)+((l_diff/20)**2))
        if diff < closest_color_diff:
            closest_color_diff =  diff
            closest_color_name = list_of_color_names[i]
    return closest_color_name
#print(sensor.color_raw)
print(closest_color(r, g, b, l))

def calibrate():
    cs = []
    for c in list_of_color_names:
        x = input(c)
        r, g, b = sensor.color_rgb_bytes
        l = int(sensor.lux)
        cs.append((r,g,b,l))
        print(r,g,b,l)
    print(cs)
#calibrate()