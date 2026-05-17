import busio
import board
import adafruit_tca9548a
import math
import adafruit_vl53l0x
import time


def setup():
    i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)  # 100000 ?
    tca = adafruit_tca9548a.TCA9548A(i2c)

    for channel in range(2,5):
        if tca[channel].try_lock():
            # addresses = tca[channel].scan()
            tca[channel].unlock()

    vlleft = adafruit_vl53l0x.VL53L0X(tca[3])
    vlfront = adafruit_vl53l0x.VL53L0X(tca[2])
    vlright = adafruit_vl53l0x.VL53L0X(tca[4])
    return vlleft, vlfront, vlright

def get_data(vl):
    ok = False
    while not ok:
        try:
            ret_value = vl.range
            ok = True
        except OSError:
            ok = False
    return ret_value

def tiles_in_dir(vl):
    dist = vl.range
    if dist > 120:
        return int((dist-120)/150)
    return 0

def at_wall(vl):
    ok = False
    while not ok:
        try:
            ret_value = (vl.range < 310)
            ok = True
        except OSError:
            ok = False
    return ret_value

# left, front, right = setup()
# while True:
#     print(get_data(left), get_data(front), get_data(right))