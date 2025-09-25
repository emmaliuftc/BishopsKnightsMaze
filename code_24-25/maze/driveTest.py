
# CORBYN'S CODE

import time
import math
from dynamixel_sdk import *
#import os
#import easyocr
#import cv2 as cv
#import numpy as np
import board
import adafruit_tca9548a
import adafruit_vl53l0x
import RPi.GPIO as GPIO

import adafruit_tcs34725
i2c = board.I2C()
tca = adafruit_tca9548a.TCA9548A(i2c)
color = adafruit_tcs34725.TCS34725(tca[3])

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

def speedup(start,end,t=0):
    packet_handler.write4ByteTxRx(port, MOTOR_LB, 104, start)
    packet_handler.write4ByteTxRx(port, MOTOR_LF, 104, start)
    packet_handler.write4ByteTxRx(port, MOTOR_RB, 104, -start)
    packet_handler.write4ByteTxRx(port, MOTOR_RF, 104, -start)
    time.sleep(1)
    packet_handler.write4ByteTxRx(port, MOTOR_LB, 104, end)
  #  packet_handler.write4ByteTxRx(port, MOTOR_LF, 104, end)
    packet_handler.write4ByteTxRx(port, MOTOR_RB, 104, -end)
  #  packet_handler.write4ByteTxRx(port, MTOR_RF, 104, -end)
    
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
        drive(250,t)
        drive(-250,t)

def drop():
    packet_handler.write4ByteTxRx(port, GEAR, 104, -100)
    time.sleep(0.86)
    packet_handler.write4ByteTxRx(port, GEAR, 104, 0)
    time.sleep(0.2)
    wiggle()
    packet_handler.write4ByteTxRx(port, GEAR, 104, 100)
    time.sleep(0.861)
    packet_handler.write4ByteTxRx(port, GEAR, 104, 0)

# initialize board


set_op_mode()
dir = 0

'''
   270
180 → 0
   90
'''

def turn_left(degrees):
    global dir
    if degrees==90:
        turn(-120, 2.6)
    dir=(dir-degrees)%360

def turn_right(degrees):
    global dir
    if degrees==90:
        turn(120, 2.6)
    elif degrees==180:
        turn(150, 4.23)
    dir=(dir+degrees)%360

#turn(120)
sta=time.time()
l=[]
c=[]
r=[]
for i in range(10):
    c.append(color.color_raw[3])
    l.append(color.lux)

drop()

#drive(-265)

#speedup(-200,-265)

#drive(-200)
#time.sleep(1.5)
#drive(150)
#time.sleep(1.2)
#drive(-265)

'''
if False:
#for i in range(10,1000):
    #m=input("mode t=turn, d=drop: ")
    x=int(input("Ready speed: "))
    #m="t"
    m=0
    start=time.time()
    #if m=="t":
   #     turn(x)
   # elif m=="d":
   #     drop()
   # else:
        drive(-x)
    #wiggle()
    #x=input("Stop")
    c.append(round(color.color_raw[3],0))
    l.append(round(color.lux,0))#
 #   r.append(round(color.color_raw[0],0))
    print(round(color.lux,0), color.color_raw,round(color.color_raw[0],0))
    #print(f"mean clear:{sum(c)/len(c)}")
    #print(f"mean lux:{sum(l)/len(l)}")
    lastfiveC = c[i-10:i]
    lastfiveL = l[i-10:i]
  #  lastfiveR = r[i-5:i]
    rollingmeanC = (sum(lastfiveC))/10
    rollingmeanL = (sum(lastfiveL))/10
    #rollingmeanR = (sum(lastfiveR))/5
    lastfiveC.sort()
    lastfiveL.sort()
   # lastfiveR.sort()
    rollingmedianC = lastfiveC[5]
    rollingmedianL = lastfiveL[5]
  #  rollingmedianR = lastfiveR[2]
    print(f"rolling mean clear: {rollingmeanC}    rolling median clear: {rollingmedianC}")
    print(f"rolling mean lux: {rollingmeanL}    rolling median lux: {rollingmedianL}")
  #  print(f"rolling mean red: {rollingmeanR}    rolling median red: {rollingmedianR}")
    x=input()
    stop()
    end=time.time()

    print(f"{end-start} seconds")
    #time.sleep(0.25)
'''
#turn_right(90)
# Release the camera and close windows
'''
x=float(input("TY"))
drive(200,x)

stop()
'''
