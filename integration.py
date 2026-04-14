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
import motor_official as motor
import multiplexer_official as plex
import math
from dynamixel_sdk import *
import os

# Motor environment setup
 
MOTOR_LB = 1
MOTOR_LF = 2
MOTOR_RB = 3
MOTOR_RF = 4
GEAR = 5
motors = [MOTOR_LB, MOTOR_LF, MOTOR_RB, MOTOR_RF, GEAR]
tires = [MOTOR_LB, MOTOR_LF, MOTOR_RB, MOTOR_RF]
port = PortHandler('/dev/ttyUSB0')
packet_handler = PacketHandler(2.0)

# Multiplexer environment setup











# Test code

motor.setup()
motor.set_op_mode()
motor.drop()


imu = plex.setup_imu()
while True:
    print(plex.imu(imu))



# while True:
# 	plex.distance(vl)
# 	plex.imu(bno)
