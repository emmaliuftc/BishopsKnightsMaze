import busio
import board
import adafruit_tca9548a
import math
import adafruit_vl53l0x



def setup():
    i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)  # 100000 ?
    tca = adafruit_tca9548a.TCA9548A(i2c)

    for channel in range(2,5):
        if tca[channel].try_lock():
            # addresses = tca[channel].scan()
            tca[channel].unlock()

    vlleft = adafruit_vl53l0x.VL53L0X(tca[2])
    vlfront = adafruit_vl53l0x.VL53L0X(tca[3])
    vlright = adafruit_vl53l0x.VL53L0X(tca[4])
    return vlleft, vlfront, vlright

def get_data(vl):
    dist = vl.range
    return dist

def tiles_in_dir(vl):
    dist = vl.range()
    return int(dist/30)