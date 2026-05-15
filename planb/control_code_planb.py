import button_planb as button
import camera_planb as camera
import color_sensor_planb as cs
import distance_sensors_planb as distance_sensors
import imu_planb as imu
import led_planb as led
import motor_official_planb as motors

import threading

motors.setup()
motors.set_op_mode()
gyro = imu.setup()
left, front, right = distance_sensors.setup()

# MAZE ALGORITHM
# LAST UPDATED - 1/19/2026 (AF)

import math
import time
'''
The main idea:
Every time we are at a new location, we look in all the directions we can look and seeing how many tiles are present. we add the positions of these tiles that we know exist to the dictionary TILES.
each tile in TILES has a dictionary with the following information:
    VISITED: boolean- have we been to this tile?
    SIDES: list of integers- each side in the order [0, 90, 180, 270]. 
    EXTRA: string with extra information- "h" for hole, "p" for puddle, etc.
At each tile, we scan all walls and then consider where to go next. This is just like last year. The only thing that has changed is how we choose where to go next

Ramps:
TBD

Different from last year: last year we had two different systems of orientation- field-based and corbyn-based. Bad. Confusing. This year, everything is field-based.
'''
n=0
u=1
w=2

# FUNCTIONS TO WRITE


# FUNCTIONS THAT WILL NEED UPDATING

def move(tile_type):
    print("moving")
    match tile_type:
        case 1:
            rots = 3725
        case 2:
            rots = 7000
        case 3:
            rots = 4953
    motors.drive()
    target_rot = motors.get_positions()[0] + rots
    print(f"target: {target_rot}")
    while motors.get_positions()[0] < target_rot:
        print(f"motor poses: {motors.get_positions()}")
    motors.stop()

    if hdg == 0:
        pos[0] += 1
    elif hdg == 90:
        pos[1] += 1
    elif hdg == 180:
        pos[0] -= 1
    elif hdg == 270:
        pos[1] -= 1


hdg = 0 
pos = [0,0]
tiles = {}

def round_nearest_90(n):
    return round(n / 90) * 90

def new_tile(posx, posy, visited, sides=[u,u,u,u]):
    global tiles
    if (posx, posy) not in tiles:
        tiles[(posx, posy)] = {"visited": visited, "sides": sides, "extra": ""} #adding new tile to dictionary tiles

def turn(turn_deg): # clockwise / right is positive
    turn_deg = turn_deg % 360
    target_imu = round_nearest_90(imu.calculate_angle(gyro)) + turn_deg
    if turn_deg == 270:
        target_imu -= 360
        motors.turn(-1)
        while imu.calculate_angle(gyro) > target_imu:
            pass
        motors.stop()
    else:
        motors.turn(1)
        while imu.calculate_angle(gyro) < target_imu:
            pass
        motors.stop()
    global hdg
    hdg = round_nearest_90(imu.calculate_angle(gyro))

def update_map():
    print("updating map")
    global tiles
    posx, posy = pos[0], pos[1]
    tiles[(posx, posy)]["visited"] = True
    new_tiles_in_dirs = {(0+hdg)%360: distance_sensors.tiles_in_dir(front), (90+hdg)%360: distance_sensors.tiles_in_dir(left), (270+hdg)%360: distance_sensors.tiles_in_dir(right)}

    if not 0==(180+hdg)%360:
        for new in range(new_tiles_in_dirs[0]):
            xc=pos[0]+new
            yc=pos[1]
            new_tile(xc,yc,False)
            tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2]=n,n
        xc=pos[0]+new_tiles_in_dirs[0]
        yc=pos[1]
        new_tile(xc,yc,False)
        tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2]=w,n
        
    if not 90==(180+hdg)%360:    
        for new in range(new_tiles_in_dirs[90]):
            xc=pos[0]
            yc=pos[1]+new
            new_tile(xc,yc,False)
            tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][3]=n,n
        xc=pos[0]
        yc=pos[1]+new_tiles_in_dirs[90]
        new_tile(xc,yc,False)
        tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][2]=w,n
        
    if not 180==(180+hdg)%360:    
        for new in range(new_tiles_in_dirs[0]):
            xc=pos[0]-new
            yc=pos[1]
            new_tile(xc,yc,False)
            tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2]=n,n
        xc=pos[0]+new_tiles_in_dirs[180]
        yc=pos[1]
        new_tile(xc,yc,False)
        tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2]=n,w
        
    if not 270==(180+hdg)%360:    
        for new in range(new_tiles_in_dirs[90]):
            xc=pos[0]
            yc=pos[1]-new
            new_tile(xc,yc,False)
            tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][3]=n,n
        xc=pos[0]
        yc=pos[1]-new_tiles_in_dirs[270]
        new_tile(xc,yc,False)
        tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][2]=n,w

def scan_and_drop():
    victim_status = camera.get_data()
    for i in range(victim_status):
        motors.drop()

def scan_tile():
    print("scanning title")
    if distance_sensors.tiles_in_dir(front) == 0:
        scan_and_drop()
    if distance_sensors.tiles_in_dir(left) == 0:
        turn(-90)
        scan_and_drop()
        turn(90)
    if distance_sensors.tiles_in_dir(right) == 0:
        turn(90)
        scan_and_drop()



def score(tilex, tiley):
    score = 0
    tile = tiles[(tilex, tiley)]
    if tile["visited"]:
        score -= 10
    score += sum(tile["sides"])
    return score

angle = [0, 0, 0]
def imu_thread():
    global angle
    while True:
        # print(f"angle: {angle}")
        start_time = time.time()
        angle, start_time = imu.calculate_angle(gyro, angle, start_time)


def find_exit_hdg():
    max_score = score(pos[0] + 1, pos[1])
    target_hdg = 0
    if score(pos[0], pos[1] + 1) > max_score:  # Check 90
        max_score = score(pos[0], pos[1] + 1)
        target_hdg = 180
    if score(pos[0] - 1, pos[1]) > max_score:  # Check 180
        max_score = score(pos[0] - 1, pos[1])
        target_hdg = 180
    if score(pos[0], pos[1] - 1) > max_score:  # Check 270
        target_hdg = 270
    return target_hdg

def main_thread():
    try:
        global tiles
        update_map()
        print("doing the main thing")
        move(1)
        print(tiles)
        
        if not tiles[tuple(pos)]["visited"]:
            update_map()
            print(tiles)
            scan_tile()
        target_hdg = find_exit_hdg()
        turn(target_hdg - hdg)
    except Exception as e:
        print(e)

main_thread()

# threads=[]
# t = threading.Thread(target=imu_thread)
# threads.append(t)
# t = threading.Thread(target=main_thread)
# threads.append(t)

# for t in threads:
#     t.start()

# for t in threads:
#     t.join()