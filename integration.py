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
import threading

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


def motor_thread():
    motor.setup()
    motor.set_op_mode()
    time.sleep(3)
    motor.kit_go_to_pos(0)
    while True:
        motor.drop()
        time.sleep(3)

def imu_thread():
    imu = plex.setup_imu()
    pos = [0,0,0]
    vel = [0,0,0]
    angle = [0,0,0]
    start_time = time.time()
    while True:
        accel_x, accel_y, accel_z = plex.accel(imu)
        gyro_x, gyro_y, gyro_z = plex.gyro(imu)
    #    print(accel_x, accel_y, accel_z)
        acc = [accel_x, accel_y, accel_z]
        gyro = [gyro_x, gyro_y, gyro_z]
        dt = time.time() - start_time
        dg = [g * dt * 180 / math.pi for g in gyro]
        angle = [x+y for x, y in zip(dg,angle)]
        dv = [a * dt for a in acc]
        vel = [x+y for x, y in zip(dv,vel)]
        dp = [v * dt for v in vel]
        pos = [x+y for x, y in zip(dp,pos)]

        start_time = time.time()
#            print(f"pos: {pos}")
#            print(f"dt: {dt}")
        print(f"acc: {acc}")
        print(f"gyro: {gyro}")
        print(f"Angle: {angle}")
# Multithreading 

exit_event = threading.Event()

def exit_worker():
    while not exit_event.is_set():
        #print("Working")
        time.sleep(1)
    print("Thread shutting down gracefully (after everythings done)")

threads = []

t = threading.Thread(target=motor_thread)
threads.append(t)
t = threading.Thread(target=imu_thread)
threads.append(t)
t = threading.Thread(target=exit_worker)
threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("I saw controlc")
    exit_event.set()
    for t in threads:
        t.join()
    print("all threads stopped :)")
