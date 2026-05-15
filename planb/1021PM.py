import button_planb as button
import camera_planb as camera
import color_sensor_planb as cs
import distance_sensors_planb as distance_sensors
import imu_planb as imu
import led_planb as led
import motor_official_planb as motors
import random
import threading

motors.setup()
motors.set_op_mode()
quat = imu.setup()
color_sensor = cs.setup()
left, front, right = distance_sensors.setup()

# MAZE ALGORITHM
# BASICALLY LAST YEAR'S CODE BUT WITH STAIRS AND RAMPS

import math
import time

print("waiting for button press")
while button.button.is_active:
    pass
while not button.button.is_active:
    pass

initial_angle = imu.get_angles(quat)[2]
time.sleep(1)

def move(tile_type):
    print("moving")
    match tile_type:
        case 0:
            rots = 3725
        case 11 | 12:
            rots = 8000
    motors.drive()
    target_rot = motors.get_positions()[0] + rots
    print(f"target: {target_rot}")
    while motors.get_positions()[0] < target_rot:
        if not going:
            break
        if cs.get_color(color_sensor) == "Black":
            reverse(target_rot - 3725)
            return
    motors.stop()
    tiles_moved = 1
    if tile_type > 10:
        tiles_moved = 2

    if hdg == 0:
        pos[0] += tiles_moved
    elif hdg == 90:
        pos[1] += tiles_moved
    elif hdg == 180:
        pos[0] -= tiles_moved
    elif hdg == 270:
        pos[1] -= tiles_moved

def reverse(target_rot):
    global state
    motors.drive(-1)
    while motors.get_positions()[0] > target_rot:
        if not going:
            break
    state = 100

hdg = 0 
pos = [0,0]
tiles_visited = []

going = True
def lop():
    global going
    global state
    print(f"Going is {going}")
    if going:
        print("stopping motors")
        motors.stop()
        going = False
        state = 100
    else:
        print("resuming")
        going = True
    print(f"Going is now {going}")

button.button.when_pressed = lop

def angle_error(target, current):
    return (target - current + 540) % 360 - 180

def turn(turn_deg): # clockwise / right is positive
    print(f"turning {turn_deg}")
    turn_deg*=-1
    global hdg
    target = (initial_angle+hdg+turn_deg) % 360 # (imu.get_angles(quat)[2]+turn_deg) % 360
    error = angle_error(target, imu.get_angles(quat)[2])
    if error < 0:
        motors.turn(1)
    else:
        motors.turn(-1)
    while abs(angle_error(target, imu.get_angles(quat)[2])) > 8:
        if not going:
            break
    motors.stop()
    hdg = (hdg - turn_deg) % 360

def scan_and_drop():
    victim_status = camera.get_data()
    led_victim()
    for i in range(victim_status):
        motors.drop()
        time.sleep(0.5)

def scan_tile():
    print("scanning title")
    if pos in tiles_visited:
        return
    tiles_visited.append(pos.copy())
    if distance_sensors.at_wall(front):
        scan_and_drop()
    if distance_sensors.at_wall(left):
        turn(-90)
        scan_and_drop()
        turn(90)
    if distance_sensors.at_wall(right):
        turn(90)
        scan_and_drop()

def one_tile_in_dir(hdg):
    if hdg == 0:
        return [pos[0]+1, pos[1]]
    elif hdg == 90:
        return [pos[0], pos[1]+1]
    elif hdg == 180:
        return [pos[0]-1, pos[1]]
    elif hdg == 270:
        return  [pos[0], pos[1]-1]

def find_exit_hdg(info=0):
    options = []
    options2 = [(hdg-180)%360]
    if not distance_sensors.at_wall(front):
        options.append(hdg)
    if not distance_sensors.at_wall(left):
        options.append((hdg-90)%360)
    if not distance_sensors.at_wall(right):
        options.append((hdg+90)%360)
    if len(options) == 0:
        return random.choice(options2)    
    print(options)
    return random.choice(options)


def get_ramp_info():
    if distance_sensors.at_wall(left) and distance_sensors.at_wall(right):
        if distance_sensors.get_data(left) + distance_sensors.get_data(right) > 600:
            print("RAMP!")
            if distance_sensors.get_data(left) > distance_sensors.get_data(right):
                return 11
            else:
                return 12
    return 0

# lop_control = threading.Event()
# going = True
# def button_thread():
#     lop_control.set()
#     global going
#     while True:
#         if button.is_pressed():
#             print(f"Button pressed!")
#             if going:
#                 going = False
#                 lop_control.clear()
#                 print("LOP CONTROL cleared")
#             else:
#                 going = True
#                 lop_control.set()
#                 print("LOP CONTROL set")
#         while button.is_pressed():
#             pass
        
state = 100
def main():
    global state
    global going
    info = 0
    while True:
        if going:
            match state:
                case 100:
                    scan_tile()
                    info = get_ramp_info()
                    target_heading = find_exit_hdg(info)
                    state = 200
                case 200:
                    turn(target_heading - hdg)
                    state = 300
                case 300:
                    move(info)
                    state = 100
        print(state, going)

led_thread = threading.Thread(target=led.flash, args=(0.5,5,))

def led_victim():
    led_thread = threading.Thread(target=led.flash, args=(0.5,5,))
    led_thread.start()

main()

# thread2 = threading.Thread(target=button_thread)

# thread1.start()
# # thread2.start()
# print(hdg, imu.get_angles(quat)[2])
# turn(180)
# print(hdg, imu.get_angles(quat)[2])