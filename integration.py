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
import multiplexer_test
import math
from dynamixel_sdk import *
import os


# Make these match the actual ID numbers.  
MOTOR_LB = 1
MOTOR_LF = 2
MOTOR_RB = 3
MOTOR_RF = 4
GEAR = 5

vl, bno = multiplexer_test.setup()

while True:
	multiplexer_test.distance(vl)
	multiplexer_test.imu(bno)
