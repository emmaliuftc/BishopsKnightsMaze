# MAZE ALGORITHM
# LAST UPDATED - 1/19/2026 (AF)

import math
import time
'''
The main idea:
Every time we are at a new location, we look in all the directions we can look and seeing how many tiles are present. we add the positions of these tiles that we know exist to the dictionary TILES.
each tile in TILES has a dictionary with the following information:
    VISITED: boolean- have we been to this tile?
    SIDES: list of integers- each side in the order [0, 90, 180, 270]. 0 = neighbor, 1 = unsure, 2 = wall (these values are subject to change)
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

def drive(): # use IMU data for consistent distance?
    pass

def turn(): # maybe use IMU data?
    pass
    update hdg

def tiles_in_dir(direction) -> int:
    '''returns how many tiles in a certain direction'''
    return


# FUNCTIONS THAT WILL NEED UPDATING

def move():
    drive()
    if hdg == 0:
        pos[0] += 1
    elif hdg == 90:
        pos[1] += 1
    elif hdg == 180:
        pos[0] -= 1
    elif hdg == 270:
        pos[1] -= 1


hdg = 0 # we are using hdg as an abbreviation for heading- using dir was bad practice bc dir() is a python function (also corbyn released an EP titled "Head First" and it's lowk not as bad as I thought)
pos = [0,0]
tiles = {}

def new_tile(pos0: int, pos1: int, visited: bool, sides=[u,u,u,u]: list) -> None:
    global tiles
    if (pos0, pos1) not in tiles:
        tiles[(pos0, pos1)] = {"visited": visited, "sides": sides, "extra": ""} #adding new tile to dictionary tiles

def update_tiles(pos: list):
    tiles[(pos[0], pos[1])]["visited"] = True

    new_tiles_in_dirs = {(0+hdg)%360: tiles_in_dir(FRONT), (90+hdg)%360: tiles_in_dir(LEFT), (270+hdg)%360: tiles_in_dir(RIGHT)}

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
        
    if not 90==(180+hdg)%360:    
        for new in range(new_tiles_in_dirs[90]):
            xc=pos[0]
            yc=pos[1]-new
            new_tile(xc,yc,False)
            tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][3]=n,n
        xc=pos[0]
        yc=pos[1]-new_tiles_in_dirs[270]
        new_tile(xc,yc,False)
        tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][2]=n,w

def scan_tile():
    # go around scanning walls


def score(tilex, tiley):
    score = 0
    tile = tiles[(tilex, tiley)]
    if tile["visited"]:
        score += 10
    score += sum(tile["sides"])

while True:
    move()

    max_score = score(pos[0]+1,pos[1])
    exit_dir = 0

    if score(pos[0],pos[1]+1)>max_score:
        exit_dir = 90

    if score(pos[0],pos[1]-1)>max_score:
        exit_dir = 180

    if score(pos[0]-1,pos[1])>max_score:
        exit_dir = 180

    
