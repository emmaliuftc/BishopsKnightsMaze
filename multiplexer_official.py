import time
import busio
import board
import adafruit_tca9548a
import adafruit_vl6180x
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
)
from adafruit_bno08x.i2c import BNO08X_I2C


i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # 100000 ?
tca = adafruit_tca9548a.TCA9548A(i2c)

for channel in range(8):
    if tca[channel].try_lock():
        print("Channel {}:".format(channel), end="")
        addresses = tca[channel].scan()
        print([hex(address) for address in addresses if address != 0x70])
        tca[channel].unlock()

def setup_imu():
    # vl1 = adafruit_vl53l0x.VL53L0X(tca[1])
    # vl2 = adafruit_vl53l0x.VL53L0X(tca[2])
    # print("Lets goooo setup is done")


    # while True:
    #    print(f"Sensor 0: {vl0.distance}") # Sensor 1: {vl1.distance}, Sensor 2: {vl2.distance}")
    #    time.sleep(0.5)

    # For each sensor, create it using the TCA9548A channel instead of the I2C object
    # vl = adafruit_vl6180x.VL6180X(tca[2])
    bno = BNO08X_I2C(tca[1])

    bno.enable_feature(BNO_REPORT_ACCELEROMETER)
    bno.enable_feature(BNO_REPORT_GYROSCOPE)
    bno.enable_feature(BNO_REPORT_MAGNETOMETER)
    bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

    # After initial setup, can just use sensors as normal.
    return bno

def setup_distance():
    vl = adafruit_vl6180x.VL6180X(tca[2])
    return vl

def distance(vl):
    print(f"Distance: {vl.range}")

def accel(bno):
    accel_x, accel_y, accel_z = bno.acceleration
    # print("Acceleration:")
    # print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
    #    print("")
    return accel_x, accel_y, accel_z

def gyro(bno):
    # print("Gyro:")
    gyro_x, gyro_y, gyro_z = bno.gyro
    # print("X: %0.6f  Y: %0.6f Z: %0.6f rads/s" % (gyro_x, gyro_y, gyro_z))
    #    print("")

    #    print("Magnetometer:")
    #    mag_x, mag_y, mag_z = bno.magnetic
    #    print("X: %0.6f  Y: %0.6f Z: %0.6f uT" % (mag_x, mag_y, mag_z))
    #    print("")
    return gyro_x, gyro_y, gyro_z

def quat(bno):
    # print("Rotation Vector Quaternion:")
    quat_i, quat_j, quat_k, quat_real = bno.quaternion
    # print("I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real))
    #    print("")
    return quat_i, quat_j, quat_k, quat_real


