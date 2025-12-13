# MAYBE NEED TO FIND THE OTHER SAMPLE CODE THAT DR J GAVE US TO TEST 
# CUZ I JUST TOOK THIS ONE FROM CORBYN'S CODE FROM LAST YEAR AND I HAVE
# NO IDEA WHETHER IT ACTUALLY WORKS
# ALSO MAYBE NEED TO TEST CHAGNING THE BAUD RATE AND OR THE USB PORT
# WHERE THE MOTOR CONTROLLER IS ATTACHED

# A

import time
import math
from dynamixel_sdk import *
import os


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
            print(f"Initial connection to motor {motor_id} successful.")
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
    
set_op_mode()
drive(150)

