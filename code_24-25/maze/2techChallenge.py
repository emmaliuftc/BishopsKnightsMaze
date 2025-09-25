# CORBYN'S CODE

import time
import math
from dynamixel_sdk import *
import os
import easyocr
import cv2 as cv
import numpy as np
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

#LOPLED
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.LOW)

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
        drive(250,t)
        drive(-250,t)

def flash_led(t=0.5):
    # LED blinks for 5 seconds
    for i in range(5):
        GPIO.output(14, GPIO.HIGH)
        time.sleep(t)
        GPIO.output(14, GPIO.LOW)
        time.sleep(t)
    
def drop():
    drive(100, 0.7)
    packet_handler.write4ByteTxRx(port, GEAR, 104, -100)
    time.sleep(0.86)
    packet_handler.write4ByteTxRx(port, GEAR, 104, 0)
    time.sleep(1)
    wiggle()
    packet_handler.write4ByteTxRx(port, GEAR, 104, 100)
    time.sleep(0.861)
    packet_handler.write4ByteTxRx(port, GEAR, 104, 0)
    drive(-100, 0.3)

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
moveTime = 2.02*0.95

def turn_left(degrees=90):
    global dir
    if degrees==90:
        turn(-120, turnTime)
    dir=(dir-degrees)%360

def turn_right(degrees=90):
    global dir
    if degrees==90:
        turn(120, turnTime)
    elif degrees==180:
        turn(120, 2*turnTime)
    dir=(dir+degrees)%360

###########################
bl_rng = [0,14]
s_rng = [50,1000]
special_rng = [41,1000]
br_rng = [15,40]
r_rng = [20,40]
w_rng = [75,90]
bu_rng = [20,40]
#######################

def move():
    global checkpoint
    global checkpoint_index
 #   global moves
    global going
    start_time = time.time()
    throughswitch = True
#    blueswitch = 0
#    cpswitch = 0
    clearvalues = []
    redvalues = []
    luxvalues = []
##############
    GPIO.output(23, GPIO.HIGH)
    while time.time()-start_time<moveTime:
        drive(200)
        colorfound = get_color()
        # get_color returns Clear, Red, Lux
        if (bl_rng[0] <= colorfound[0] <= bl_rng[1]): # red or black
            print("Hole detected")
            end_time = time.time()-start_time
            drive(-200, end_time)
            neighbors = get_neighbors()
            holes.append(neighbors[1])
            throughswitch = False
            return "nothing"
        else:
            clearvalues.append(colorfound[0])
            redvalues.append(colorfound[1])
            luxvalues.append(colorfound[2])
#        elif get_color() == "bu":
#            blueswitch += 1
#        elif get_color() == "s":
#            cpswitch += 1
#        print(f"gce: ({get_color()})")
        if (br_rng[0] <= colorfound[0] <= br_rng[1]) and (colorfound[1] > 12):
            print("Red found")
        if GPIO.input(BUTTON) == GPIO.HIGH:
            lop_activated()
            throughswitch = False
########
    GPIO.output(23, GPIO.LOW)
    if throughswitch:
#        print(blueswitch, cpswitch, 5678)
        stop()
        if dir == 0:
            pos[0] += 1
        elif dir == 90:
            pos[1] -= 1
        elif dir == 180:
            pos[0] -= 1
        elif dir == 270:
            pos[1] += 1
        moves.append(dir)
        print(f"individual color values collected: {len(clearvalues)}")
        backclearvalues = clearvalues[2*len(clearvalues)//3:]
        backredvalues = redvalues[2*len(redvalues)//3:]
        backluxvalues = luxvalues[2*len(luxvalues)//3:]
        backclearvalues.sort()
        backredvalues.sort()
        backluxvalues.sort()
        clear = backclearvalues[len(backclearvalues)//2]
        red = backredvalues[len(backredvalues)//2]
        lux = backluxvalues[len(backluxvalues)//2]
        if special_rng[0] <= clear <= special_rng[1]:
            if lux<2500:
                print("saw silver in 75-90 range")
                print("CHECKPOINT DETECTED")
                going=False
                
                scanned_tiles.append(pos.copy())
                checkpoint = pos.copy()
                checkpoint_index = len(moves)
                return "checkpoint"
            else:
                print("saw white in 75-90 range")
                print("No checkpoint detected")
        elif br_rng[0] <= clear <= br_rng[1]:
            if red > 12:
                print("saw red in special range")
                return "right"
            else:
                print("saw blue in special range")
                return "left"
        elif bl_rng[0] <= clear <= bl_rng[1]:
            print("saw black, THIS SHOULD NEVER HAPPEN, IF YOU SEE THIS SOMETHING WENT HORRIBLY WRONG")
#        if s_rng[0] <= clear <= s_rng[1]:
#            print("saw silver")
#            return "s"
#        elif r_rng[0] <= clear <= r_rng[1]:
#           print("saw red")
#        elif bu_rng[0] <= clear <= bu_rng[1]:
#            print("saw blue")
        elif w_rng[0] <= clear <= w_rng[1]:
            print("saw white")
            print("No checkpoint detected")
            return "nothing"

        else:
            print("saw no color what the ???")
            print(f"clear:{clear}, red:{red}, lux{lux}")
            return "nothing"
'''
        if cpswitch>1:
            print("CHECKPOINT DETECTED")
            scanned_tiles.append(pos.copy())
            checkpoint = pos.copy()
            checkpoint_index = len(moves)
        else:
            print("No checkpoint detected")
 
        if blueswitch>1:
            scanned_tiles.append(pos.copy())
            time.sleep(5)
'''

def explore():
    moves.append(dir)
    global checkpoint
    global checkpoint_index
    global moves
    global going
    start_time = time.time()
    throughswitch = True
#    blueswitch = 0
#    cpswitch = 0
    clearvalues = []
    redvalues = []
    luxvalues = []
##############
    GPIO.output(23, GPIO.HIGH)
    while time.time()-start_time<moveTime:
        drive(200)
        

# initialize and turn on camera
image = cv.VideoCapture(0)

def lop_activated():
    global pos
    global moves
    while GPIO.input(BUTTON) == GPIO.HIGH:
        time.sleep(0.01)
    stop()
    print("LOP ACTIVATED")
    pos = checkpoint.copy()
    moves=moves[:checkpoint_index]
    while GPIO.input(BUTTON) == GPIO.LOW:
        time.sleep(0.01)
    while GPIO.input(BUTTON) == GPIO.HIGH:
        time.sleep(0.01)
    if toggler%2==1:
        turn_left(90)
    else:
        turn_right(90)

def detect_color(image):
    colors_detected = []
    number_red_detected = 0
    number_yellow_detected = 0
    number_green_detected = 0
    number_black_detected = 0
    
    # loop to capture and process frames
    for i in range(150):
        if not image.isOpened():
            print("Cannot open camera")
            exit()

        # Define color ranges (in HSV)
        lower_red1 = np.array([0, 150, 50])
        upper_red1 = np.array([10, 255, 150])
        lower_red2 = np.array([170, 150, 150]) 
        upper_red2 = np.array([179, 255, 255])
        lower_yellow = np.array([20, 80, 100])
        upper_yellow = np.array([30, 255, 255])
        lower_green = np.array([35, 80, 60])
        upper_green = np.array([85, 255, 255])
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])

        # Capture frame
        ret, frame = image.read()
        if not ret:
            print("Cannot receive frame (stream end?). Exiting...")
            break

        # Convert to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create a mask for all victim colors
        red_mask1 = cv.inRange(hsv, lower_red1, upper_red1)
        red_mask2 = cv.inRange(hsv, lower_red2, upper_red2)
        yellow_mask = cv.inRange(hsv, lower_yellow, upper_yellow)
        green_mask = cv.inRange(hsv, lower_green, upper_green)
        black_mask = cv.inRange(hsv, lower_black, upper_black)
        # count number of victim colored pixels
        num_red_pixels = np.sum(red_mask1 == 255) + np.sum(red_mask2 == 255)
        num_yellow_pixels = np.sum(yellow_mask == 255)
        num_green_pixels = np.sum(green_mask == 255)
        num_black_pixels = np.sum(black_mask == 255)
        # check colored pixels and record in list
        if num_red_pixels > 5000:
            number_red_detected +=1
            if "red" not in colors_detected:
                colors_detected.append("red")
       
        if num_yellow_pixels > 5000:
            number_yellow_detected +=1
            if "yellow" not in colors_detected:
                colors_detected.append("yellow")
          
        if num_green_pixels > 6000: 
            number_green_detected +=1
            if "green" not in colors_detected:
                colors_detected.append("green")
        
        if num_black_pixels > 3000:
            number_black_detected +=1 
            if "black" not in colors_detected:
                colors_detected.append("black")
            
        # Display the original image and the mask
        # cv.imshow("Original", frame)
        # cv.imshow("Mask", red_mask1)
        
        # print(f"HSV:{hsv}")
        # print(f"Mask: {red_mask}")
        # print(f"Colors_Detected: {colors_detected}")
        
        # Exit on 'q' key press
        # if cv.waitKey(1) & 0xFF == ord('q'):
            # break

    # print(number_red_detected, number_yellow_detected, number_green_detected)
    print(f"number of black pixels: {num_black_pixels}")
    if number_red_detected > 100:
        color = "red"
    elif number_yellow_detected > 100:
        color = "yellow"
    elif number_green_detected > 100:
        color = "green"
    elif number_black_detected > 100:
        color = "black"
    else:
        color = "none"
    # print(f"COLOR RETURNING: {color}")
    return color

    
def detect_letter(image):
    try:
        # reading English characters and set up image
        reader = easyocr.Reader(['en'])
        if not image.isOpened():
            print("Cannot open camera")
            exit()

        # get a frame
        start = time.perf_counter()
        ret, frame = image.read()
        if not ret:
            print("Cannot receive frame (stream end?). Exiting...")
            exit()
        next_time = time.perf_counter()
        print(f"Time to get this frame: {next_time - start} seconds")

        # resize to smaller frame
        start = time.perf_counter()
        frame = cv.resize(frame, (100, 100))
        next_time = time.perf_counter()
        print(f"Time to resize frame: {next_time - start} seconds")
        
        # checked all rotations and letter is not a victim
        # look for letter
        start = time.perf_counter()
        print("Got frame, looking for text...")
        result = reader.readtext(frame)
        next_time = time.perf_counter()
        print(f"Time to find letter(s): {next_time - start} seconds")
        #print(result)
        cv.imwrite("another_captured_image.jpg", frame)
        
        degrees = 0
        if len(result) == 0:
            while degrees != 100:
                if degrees == 0:
                    degrees = 30
                elif degrees == 30:
                    degrees = -60
                elif degrees == -60:
                    degrees = 100
                print(degrees)
                # rotate image
                height, width = frame.shape[:2]
                center = (width // 2, height // 2)
                scale = 1.0
                M = cv. getRotationMatrix2D(center, degrees, scale)
                rotated_image = cv.warpAffine(frame, M, (width, height))
                cv.imwrite("rotated_image.jpg", rotated_image)
                # look for letter
                start = time.perf_counter()
                print("Got frame, looking for text...")
                result = reader.readtext(rotated_image)
                next_time = time.perf_counter()
                print(f"Time to find letter(s): {next_time - start} seconds")
                print(result)
                if len(result) == 0:
                    print("no letter seen")
                    letter = "nothing"
                else:
                    letter = result[0][1]
                    # check if an actual victim
                    # if letter in ("H", "S", "U"):
                        # print(f"letter:{letter}")
                        # return letter
                    # up for changing, depends how the rotations are
        else:
            letter = result[0][1]
            
        # account for rotations and return correct letter
        if letter in ("H", "K"):
            return "H"
        elif letter in ("S", "5", "0)", "6", "0", "8"):
            return "S"
        elif letter in ("U", "3", "C"):
            return "U"
        else:
            return f"{letter} is not a victim"
            
        # Exit on 'q' key press
        #if cv.waitKey(1) & 0xFF == ord('q'):
            #exit()

    
    except IndexError:
        return "index error"


def scan():
    recalibrate()
    color = detect_color(image)
    print(color)
    if color == "red":
        print("sees red")
        flash_led()
        drop()
    elif color == "yellow":
        print("sees yellow")
        flash_led()
        drop()
    elif color == "green":
        print("sees green")
        flash_led()
        drop()
    elif color == "black":
        print("no color victim seen")
        print("sees letter, hopefully")
        flash_led()
        '''
        letter = detect_letter(image)
        print(letter)
        if letter == "H":
            flash_led()
            drop()
            drop()
        elif letter == "S":
            flash_led()
            drop()
        elif letter == "U":
            flash_led()
        '''
    elif color == "none":
        print("no letter or color victim seen")

def scan_tile(exitDir, atWalls):
    if exitDir == 90:
        if atWalls["left"]:
            turn_left(90)
            scan()
            turn_right(90)
        if atWalls["front"]:
            scan()
        turn_right(90)
    
    elif exitDir == 180:
        if atWalls["front"]:
            scan()
        if atWalls["right"]:
            turn_right(90)
            scan()
            if atWalls["left"]:
                turn_right(180)
                scan()
                turn_left(90)
        elif atWalls["left"]:
            turn_left(90)
            scan()
            turn_left(90)

    elif exitDir == 270:
        if atWalls["right"]:
            turn_right(90)
            scan()
            turn_left(90)
        if atWalls["front"]:
            scan()
        turn_left(90)

    else:
        if atWalls["left"]:
            turn_left(90)
            scan()
            turn_right(90)
        if atWalls["right"]:
            turn_right(90)
            scan()
            turn_left(90)
        
    scanned_tiles.append(pos.copy())

wall_buffer = 20

def recalibrate():
    drive(150, 2)
    drive(-100, 0.65)

def atWall(sensor):
    #x=input(f"Is there a wall on the {sensor}? ")
    if sensor=="right":
    	print(f"Right: {R.distance}")
    	
    	if R.distance<wall_buffer:
    		print("wall right")
    	else:
    		print("no wall right")
    	return R.distance<wall_buffer
    elif sensor=="front":
    	print(f"Front: {F.distance}")
    	if F.distance<wall_buffer:
    		print("wall front")
    	else:
    		print("no wall front")
    	return F.distance<wall_buffer
    elif sensor=="left":
    	print(f"Left: {L.distance}")
    	if L.distance<wall_buffer:
    		print("wall left")
    	else:
    		print("no wall left")
    	return L.distance<wall_buffer

toggler=0
def toggle():
    global toggler
    print(f"toggle: {toggler}")
    if toggler % 2 == 1:
        recalibrate()
    toggler += 1

def get_neighbors():
    if dir == 0:
        neighbors = [[pos[0],pos[1]+1], [pos[0]+1,pos[1]], [pos[0],pos[1]-1]]
    if dir == 90:
        neighbors = [[pos[0]+1,pos[1]], [pos[0],pos[1]-1], [pos[0]-1,pos[1]]]
    if dir == 180:
        neighbors = [[pos[0],pos[1]-1], [pos[0]-1,pos[1]], [pos[0],pos[1]+1]]
    if dir == 270:
        neighbors = [[pos[0]-1,pos[1]], [pos[0],pos[1]+1], [pos[0]+1,pos[1]]]
    return neighbors.copy()

def find_exitDir(pathWalls):
    if not pathWalls["right"]:
        exitDir = 90
    elif pathWalls["front"] and pathWalls["left"]:
        exitDir = 180
    elif pathWalls["front"]:
        exitDir = 270
    else:
        exitDir = 0
        
    neighbors = get_neighbors()
    
    if exitDir == 90 and neighbors[2] in scanned_tiles:
        if not pathWalls["front"] and neighbors[1] not in scanned_tiles:
            exitDir = 0
        elif not pathWalls["left"] and neighbors[0] not in scanned_tiles:
            exitDir = 270
    if exitDir == 0 and neighbors[1] in scanned_tiles:
        if not pathWalls["left"] and neighbors[0] not in scanned_tiles:
            exitDir = 270
        elif not pathWalls["right"] and neighbors[2] not in scanned_tiles:
            exitDir = 90
    if exitDir == 270 and neighbors[0] in scanned_tiles:
        if not pathWalls["right"] and neighbors[2] not in scanned_tiles:
            exitDir = 90
        elif not pathWalls["front"] and neighbors[1] not in scanned_tiles:
            exitDir = 0
        
    
    
    return exitDir

def get_pathWalls():
    neighbors = get_neighbors()
    return {"left": atWall("left") or neighbors[0] in holes, "front": atWall("front") or neighbors[1] in holes, "right": atWall("right") or neighbors[2] in holes}

def get_atWalls():
    return {"left": atWall("left"), "front": atWall("front"), "right": atWall("right")}

def go():
    if going:
        if move()=="right":
            if atWall("right"):
                turn_left()
            else:
                turn_right()
        elif move()=="left":
            if atWall("left"):
                turn_right()
            else:
                turn_left()
    else:
        atWalls = get_atWalls()
        explore()
        if atWalls["left"]:
            turn_left()
            scan()
            turn_right()
        if atWalls["right"]:
            turn_right()
            scan()
            turn_left()
        if atWalls["front"]:
            scan()
            if atWalls["left"] and not atWalls["right"]:
                turn_right()
            elif atWalls["right"] and not atWalls["left"]:
                turn_left()
            
    
def get_color():
    clear = color.color_raw[3]
    red = color.color_raw[0]
    lux = color.lux
    return clear,red,lux
'''
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
'''
'''
    else:
        readings = []
        lux_readings = []
        red_readings = []
        for i in range(m):
            readings.append(color.color_raw[3])
            lux_readings.append(color.lux)
            red_readings.append(color.color_raw[0])
            time.sleep(0.025)
        readings.sort()
        lux_readings.sort()
        red_readings.sort()
        clear = readings[int(len(readings)/2)] #sum(readings)/m # sorted(readings)[m//2]
        lux = lux_readings[int(len(lux_readings)/2)]
        red = red_readings[int(len(red_readings)/2)]
        print(f"Median color reading: {clear}")
        print(f"Median lux reading: {round(lux,1)}")
        if special_rng[0] <= clear <= special_rng[1]:
            if lux<2500:
                print("saw silver in 75-90 range")
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
#        if s_rng[0] <= clear <= s_rng[1]:
#            print("saw silver")
#            return "s"
        if r_rng[0] <= clear <= r_rng[1]:
            print("saw red")
            return "r"
        if bu_rng[0] <= clear <= bu_rng[1]:
            print("saw blue")
            return "bu"
        if w_rng[0] <= clear <= w_rng[1]:
            print("saw white")
            return "w"
    '''

def return_to_start():
    global going
    going = False
    print("returning to start")
    print(f"moves: {moves}; len {len(moves)}")
    moves.reverse()
    print(f"NEW MOVES: {moves}")
    for n in moves:
        print(f"n = {n}")
        goal_dir = (n-180)%360
        exitDir = (goal_dir - dir)%360
        print(f"goal_dirL {goal_dir}; exitDir: {exitDir}; dir: {dir}; pos: {pos}")
        if exitDir==270:
            turn_left(90)
        else:
            turn_right(exitDir)
        drive(200, driveTime)
        if atWall("front"):
            recalibrate()
    if atWall("right"):
        turn_left()
    elif atWall("left"):
        turn_right()
    drive(265, 7)
    flash_led(1)
        
    
while GPIO.input(BUTTON) == GPIO.LOW:
    time.sleep(0.01)
while GPIO.input(BUTTON) == GPIO.HIGH:
    time.sleep(0.01)

while not atWall("front"):
    drive(150, 10)
recalibrate()
if atWall("left"):
    turn_right()
elif atWall("right"):
    turn_left()

going = True
while True:
    go()
    #print(f"time remaining: {run_start-time.time()+run_length}")
#return_to_start()
