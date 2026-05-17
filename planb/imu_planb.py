import busio
import board
import adafruit_tca9548a
import math
import time
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR
)
from adafruit_bno08x.i2c import BNO08X_I2C



def setup():
    i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)  # 100000 ?
    tca = adafruit_tca9548a.TCA9548A(i2c)

    if tca[6].try_lock():
        # addresses = tca[channel].scan()
        tca[6].unlock()

        bno = BNO08X_I2C(tca[6])
        bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
    return bno


def quat_to_euler(w, x, y, z):
    # roll (x-axis)
    roll = math.atan2(
        2.0 * (w * x + y * z),
        1.0 - 2.0 * (x * x + y * y)
    )

    # pitch (y-axis)
    pitch = math.asin(
        2.0 * (w * y - z * x)
    )

    # yaw (z-axis)
    yaw = math.atan2(
        2.0 * (w * z + x * y),
        1.0 - 2.0 * (y * y + z * z)
    )

    return roll, pitch, yaw

def get_angles(sensor):


    ok = False
    while not ok:
        try:
            x, y, z, w = sensor.quaternion
            roll, pitch, yaw = quat_to_euler(w, x, y, z)

            # convert to degrees
            roll = math.degrees(roll)
            pitch = math.degrees(pitch)
            yaw = 0-math.degrees(yaw)
            if yaw < 0:
                yaw += 360
            ok = True
        except OSError:
            ok = False
    return roll, pitch, yaw
    
# a = setup()
# pvs = a.quaternion
# while True:
#     q = a.quaternion
#     print([q[i] - pvs[i] for i in range(4)])
#     pvs = a.quaternion
#     time.sleep(1)