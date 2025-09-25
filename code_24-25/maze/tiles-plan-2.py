def move():
    global checkpoint
    global checkpoint_index
    global moves
    start_time = time.time()
    throughswitch = True

##############
    while time.time()-start_time < moveTime/2:
        drive(200)
        if get_color() == "bl" or get_color() == "r":
            print("Hole or danger zone detected")
            end_time = time.time()-start_time
            drive(-200, end_time)
            neighbors = get_neighbors()
            holes.append(neighbors[1])
            throughswitch = False
            break

    total_colors_detected = []
    while time.time()-moveTime/2 < moveTime:
        drive(200)
        colorfound = get_color()
        if colorfound == "bu":
            print("BLUE")
            total_colors_detected.append("blue")
        
        elif colorfound == "si":
            print("SILVER")
            total_colors_detected.append("silver")

        elif colorfound == "w":
            print("WHITE")
            total_colors_detected.append("white")
    
    final_color = mode(total_colors_detected)
    if final_color == "blue":
        scanned_tiles.append(pos.copy())
        time.sleep(5)
    elif final_color == "silver":
        print('CHECKPOINT DETECTED')
        scanned_tiles.append(pos.copy())
        checkpoint = pos.copy()
        checkpoint_index = len(moves)
    elif final_color == "white":
        print("no checkpoint detected")


    
    if GPIO.input(BUTTON) == GPIO.HIGH:
        lop_activated()
        throughswitch = False

### if on a new tile
    if throughswitch:
        stop()
        if dir == 0:
            pos[0] += 1
        elif dir == 90:
            pos[1] -= 1
        elif dir == 180:
            pos[0] -= 1
        elif dir == 270:
            pos[1] += 1
        if going:
            moves.append(dir)
            if pos == checkpoint:
                moves=moves[:checkpoint_index]

###########################
bl_clear_rng = [0,10]
s_clear_rng = [50,1000]
special_clear_rng = [41,90]
br_clear_rng = [20,40]
r_clear_rng = [20,40]
w_clear_rng = [75,90]
bu_clear_rng = [20,40]
###########################
def get_color():

    detected_colors = []
    total_clear = 0
    total_red = 0
    total_lux = 0
    num=10
    for i in range(num):
        clear_reading = color.color_raw[3]
        red_reading = color.color_raw[0]
        lux_reading = color.lux

        total_clear += clear_reading
        total_red += red_reading
        total_lux += lux_reading

    clear_average = clear/num
    red_average = red/num
    lux_average = lux/num

    # differentiate silver and white
    if 82 < clear_average < 90 and lux_average > 2500:
        detected_colors.append('w')
    elif 75 < clear_average < 82 and lux_average < 2500:
        detected_colors.append('si')
    
    # differentiate red and blue
    if 22 < clear_average < 32 and 14 < red_average < 24:
        detected_colors.append('r')
    elif 22 < clear_average < 32 and red_average < 10:
        detected_colors.append('bu')

    if 0 < clear_average < 10:
        detected_colors.append('bl')
    
    # check for max color
    color = mode(detected_colors)
    print(f"return value for get_color: {color}")
    return color
