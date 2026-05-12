import busio
import board
import adafruit_tca9548a
import math
import adafruit_tcs34725


def setup():
    i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)  # 100000 ?
    tca = adafruit_tca9548a.TCA9548A(i2c)

    if tca[5].try_lock():
        # addresses = tca[channel].scan()
        tca[5].unlock()

    color = adafruit_tcs34725.TCS34725(tca[5])

def get_color(sensor):        
    r, g, b, c = sensor.color_raw
    color = "White"
    return color