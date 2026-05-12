if not 0 == (180+hdg)%360:    
    for new in range(new_tiles_in_dirs[0]):
        xc = self.pos[0]+new
        yc = self.pos[1]
        new_tile(xc,yc,False)
        tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2] = self.TILE_N,self.TILE_N
    xc = self.pos[0]+new_tiles_in_dirs[0]
    yc = self.pos[1]
    new_tile(xc,yc,False)
    tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2] = self.TILE_W,self.TILE_N
    
if not 90 == (180+hdg)%360:    
    for new in range(new_tiles_in_dirs[90]):
        xc = self.pos[0]
        yc = self.pos[1]+new
        new_tile(xc,yc,False)
        tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][3] = self.TILE_N,self.TILE_N
    xc = self.pos[0]
    yc = self.pos[1]+new_tiles_in_dirs[90]
    new_tile(xc,yc,False)
    tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][2] = self.TILE_W,self.TILE_N
    
if not 180 == (180+hdg)%360:    
    for new in range(new_tiles_in_dirs[180]):
        xc = self.pos[0]-new
        yc = self.pos[1]
        new_tile(xc,yc,False)
        tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2] = self.TILE_N,self.TILE_N
    xc = self.pos[0]+new_tiles_in_dirs[180]
    yc = self.pos[1]
    new_tile(xc,yc,False)
    tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2] = self.TILE_N,self.TILE_W
    
if not 90 == (180+hdg)%360:    
    for new in range(new_tiles_in_dirs[90]):
        xc = self.pos[0]
        yc = self.pos[1]-new
        new_tile(xc,yc,False)
        tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][3] = self.TILE_N,self.TILE_N
    xc = self.pos[0]
    yc = self.pos[1]-new_tiles_in_dirs[270]
    new_tile(xc,yc,False)
    tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][2] = self.TILE_N,self.TILE_W