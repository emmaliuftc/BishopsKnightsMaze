import busio
import board
import adafruit_tca9548a
import math
import time
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
)
from adafruit_bno08x.i2c import BNO08X_I2C



def setup():
    i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)  # 100000 ?
    tca = adafruit_tca9548a.TCA9548A(i2c)

    if tca[6].try_lock():
        # addresses = tca[channel].scan()
        tca[6].unlock()

        bno = BNO08X_I2C(tca[6])
        bno.enable_feature(BNO_REPORT_ACCELEROMETER)
        bno.enable_feature(BNO_REPORT_GYROSCOPE)
        bno.enable_feature(BNO_REPORT_MAGNETOMETER)
        bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
    return bno



def calculate_angle(sensor, angle, start_time):

    gyro_x, gyro_y, gyro_z = sensor.gyro
    gyro = [gyro_x, gyro_y, gyro_z]
    dt = time.time() - start_time
    start_time = time.time()
    dg = [g * dt * 180 / math.pi for g in gyro]
    angle = [x+y for x, y in zip(dg, angle)]
    return angle, start_time