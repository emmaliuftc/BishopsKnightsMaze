# CORBYN'S CODE

import time
import math
from dynamixel_sdk import *
import numpy as np
import board
import adafruit_tca9548a
import adafruit_vl53l0x
import RPi.GPIO as GPIO

import adafruit_tcs34725
i2c = board.I2C()
tca = adafruit_tca9548a.TCA9548A(i2c)
color = adafruit_tcs34725.TCS34725(tca[3])

GPIO.setup(18, GPIO.IN)

# LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, GPIO.LOW)

# Make these match the actual ID numbers.  
MOTOR_LB = 1
MOTOR_LF = 2
MOTOR_RB = 3
MOTOR_RF = 4
GEAR = 5
BUTTON = 18

GPIO.setup(BUTTON, GPIO.IN)

# If you have more/fewer than 4 motors make sure to adjust this list
motors = [MOTOR_LB, MOTOR_LF, MOTOR_RB, MOTOR_RF, GEAR]

# This identifies the USB port where the motor controller is attached
port = PortHandler('/dev/ttyUSB0')
# This object contains the methods for reading/writing
packet_handler = PacketHandler(2.0)

# Start up both handlers
print("Opening USB port and establishing connection...\n")
port.openPort()
port.setBaudRate(57600)

# Read the ID numbers from the motor memory to test connection.
# Count how many successes to make sure that all are successes.
print("Test reading from each motor:")
read_success = 0
while read_success < len(motors):
    for motor in motors:
        # ID is 1 byte, stored at memory address 7.
        motor_id, result, error = packet_handler.read1ByteTxRx(
                port, motor, 7)
        if result != COMM_SUCCESS:
            print("Read result was not a success.  The SDK says:")
            print(f"{packet_handler.getTxRxResult(result)}") 
        elif error != 0:
            print("Error found in reading.  The SDK says:")
            print(f"{packet_handler.getRxPacketError(error)}")
        else:
            # print(f"Initial connection to motor {motor_id} successful.")
            read_success += 1
    if read_success < len(motors):
        print("Not all motors succeeded.  Retrying in 1 second.\n\n")
        time.sleep(1)

# Set operating mode to extended position
def set_op_mode():
    for motor in motors:
        packet_handler.write1ByteTxRx(port, motor, 64, 0)
        packet_handler.write1ByteTxRx(port, motor, 11, 1)
        packet_handler.write1ByteTxRx(port, motor, 64, 1)
    time.sleep(0.1)

def drive(vel, t=0):
    if t==0:
        packet_handler.write4ByteTxRx(port, MOTOR_LB, 104, vel)
        packet_handler.write4ByteTxRx(port, MOTOR_LF, 104, vel)
        packet_handler.write4ByteTxRx(port, MOTOR_RB, 104, -vel)
        packet_handler.write4ByteTxRx(port, MOTOR_RF, 104, -vel)
    else:
        drive(vel)
        time.sleep(t)
        stop()

def stop():
    drive(0)
 
def turn(vel, t=0):
    if t==0:
        packet_handler.write4ByteTxRx(port, MOTOR_LB, 104, vel)
        packet_handler.write4ByteTxRx(port, MOTOR_LF, 104, vel)
        packet_handler.write4ByteTxRx(port, MOTOR_RB, 104, vel)
        packet_handler.write4ByteTxRx(port, MOTOR_RF, 104, vel)
    else:
        turn(vel)
        time.sleep(t)
        stop()

def measure():
    positions = []
    pos,_,_ = packet_handler.read4ByteTxRx(port, MOTOR_LB, 132)
    positions.append(pos)
    pos,_,_ = packet_handler.read4ByteTxRx(port, MOTOR_LF, 132)
    positions.append(pos)
    pos,_,_ = packet_handler.read4ByteTxRx(port, MOTOR_RB, 132)
    positions.append(pos)
    pos,_,_ = packet_handler.read4ByteTxRx(port, MOTOR_RF, 132)
    positions.append(pos)
    pos,_,_ = packet_handler.read4ByteTxRx(port, GEAR, 132)
    positions.append(pos)
    return positions

def wiggle():
    t=0.005
    for i in range(7):
        drive(220,t)
        drive(-220,t)

def flash_led(t=0.5):
    # LED blinks for 5 seconds
    for i in range(5):
        GPIO.output(14, GPIO.HIGH)
        time.sleep(t)
        GPIO.output(14, GPIO.LOW)
        time.sleep(t)
    
def drop():
    packet_handler.write4ByteTxRx(port, GEAR, 104, -100)
    time.sleep(0.86)
    packet_handler.write4ByteTxRx(port, GEAR, 104, 0)
    time.sleep(1)
    wiggle()
    packet_handler.write4ByteTxRx(port, GEAR, 104, 100)
    time.sleep(0.861)
    packet_handler.write4ByteTxRx(port, GEAR, 104, 0)

# initialize board

L = adafruit_vl53l0x.VL53L0X(tca[0])
F = adafruit_vl53l0x.VL53L0X(tca[1])
R = adafruit_vl53l0x.VL53L0X(tca[2])

pos = [0,0]
scanned_tiles = []
set_op_mode()
dir = 0
holes = []
checkpoint = [0,0]
moves = []
checkpoint_index = 0
'''
   270
180 → 0
   90
'''

run_length = 400

turnTime = 2.55
moveTime = 1.95*0.9

def turn_left(degrees):
    global dir
    if degrees==90:
        turn(-120, turnTime)
    dir=(dir-degrees)%360

def turn_right(degrees):
    global dir
    if degrees==90:
        turn(120, turnTime)
    elif degrees==180:
        turn(120, 2*turnTime)
    dir=(dir+degrees)%360


###########################
bl_rng = [0,10]
s_rng = [50,1000]
special_rng = [41,90]
br_rng = [20,40]
r_rng = [20,40]
w_rng = [75,90]
bu_rng = [20,40]
###########################
def get_color():
    if 1==1:
        clear = color.color_raw[3]
        red = color.color_raw[0]
        lux = color.lux
        
        if special_rng[0] <= clear <= special_rng[1]:
            if lux<2500:
                print("sawr silver in 75-90 range")
                return "s"
            else:
                print("saw white in 75-90 range")
                return "w"
        if br_rng[0] <= clear <= br_rng[1]:
            if red > 12:
                print("saw red in special range")
                return "r"
            else:
                print("saw blue in special range")
                return "bu"
        if bl_rng[0] <= clear <= bl_rng[1]:
            print("saw black")
            return "bl"
        if s_rng[0] <= clear <= s_rng[1]:
            print("saw silver")
            return "s"
        if r_rng[0] <= clear <= r_rng[1]:
            print("saw red")
            return "r"
        if bu_rng[0] <= clear <= bu_rng[1]:
            print("saw blue")
            return "bu"
        if w_rng[0] <= clear <= w_rng[1]:
            print("saw white")
            return "w"
bcount = 0
scount = 0
startT = time.time()
while True:
    n=0
    while GPIO.input(18)==0:
        pass
    while GPIO.input(18)==1:
        GPIO.output(14, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(14, GPIO.LOW)
        time.sleep(0.5)
        n+=1
    if n%4==1:
        drive(120)
    elif n%4==2:
        drive(-120) 
    elif n%4==3:
        turn(-150)
    else:
        turn(150)
    while GPIO.input(18)==0:
        pass
    stop()
    while GPIO.input(18)==1:
        pass
