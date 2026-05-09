# Edge Impulse - OpenMV Image Classification Example
#
# This work is licensed under the MIT license.
# Copyright (c) 2013-2024 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE

# Im prettys ure that this is the most updated one.... I lowkey have no idea though

import sensor, time, ml, uos, gc, pyb, math

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

net = None
labels = None

vcp = pyb.USB_VCP()
led = pyb.LED(3)

led.toggle()

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = ml.Model("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    print(e)
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

clock = time.clock()

led.toggle()
colors = {"Yellow": (148, 134, 58),"Red":(82, 12, 16),"Blue":(16, 57, 115),"Green":(0, 36, 16),"Black":(0,8,0)}
list_of_color_names = ["Yellow", "Red", "Blue", "Green", "Black"]
list_of_color_rgb_tuples = [(148, 134, 58), (82, 12, 16), (16, 57, 115), (0, 36, 16), (0,8,0)]

def closest_color(r, g, b):
    closest_color_diff = 1000000
    closest_color_name = "Uknown"
    for i in range(len(list_of_color_rgb_tuples)):
        red_diff = r - list_of_color_rgb_tuples[i][0]
        green_diff = g - list_of_color_rgb_tuples[i][1]
        blue_diff = b - list_of_color_rgb_tuples[i][2]
        diff = math.sqrt((red_diff*red_diff)+(green_diff*green_diff)+(blue_diff*blue_diff))
        if diff < closest_color_diff:
            closest_color_diff =  diff
            closest_color_name = list_of_color_names[i]
    return closest_color_name

def mode(data):
    counts = {}
    for x in data:
        counts[x] = counts.get(x,0) + 1
    max_count = max(counts.values())
    for x in counts:
        if counts[x] == max_count:
            return x

while(True):
    led.toggle()
    img = sensor.snapshot()
    img.lens_corr()
    # sensor.flush()
    # detect dark blobs
    circles = img.find_circles(threshold = 5000, x_margin = 0, y_margin = 0)
    ring_colors = []
    if circles:
        # print(len(circles), circles)
        lar_c = max(circles, key=lambda c:c.r())
        radius = lar_c.r()/5
        rings = [[] for _ in range(5)]
        # img.draw_circle(lar_c.x(), lar_c.y(), lar_c.r(), color = 255)
        # sensor.flush()
        for i in range(5):
            ring = i+1
            # print(f'ring{ring}')
            temp_radius = i*radius + radius/2
            for j in range(90):
                angle = math.pi/45*j
                pixel_loc = (lar_c.x() + int(temp_radius*math.cos(angle)), lar_c.y() + int(temp_radius*math.sin(angle)))
                pixel_rgb = img.get_pixel(pixel_loc[0], pixel_loc[1])
                pixel_color = closest_color(pixel_rgb[0], pixel_rgb[1], pixel_rgb[2])
                # print(f"pixel:{pixel_loc}, color:{pixel_color}")
                # img.draw_cross(pixel_loc[0], pixel_loc[1], tuple(255 - x for x in colors[pixel_color]), size=2)
                rings[i].append(pixel_color)
            # sensor.flush()
        # time.sleep(2)
        for r in rings:
            # print(mode(r))
            ring_colors.append(mode(r))
        # sensor.flush()
        total = 0
        for color in ring_colors:
            if color == "Black":
                total -= 2
            elif color == "Yellow":
                total += 0
            elif color == "Green":
                total += 1
            elif color == "Blue":
                total += 2
            elif color == "Red":
                total -= 1
            else:
                ...
        vcp.write(f"Target:{total}\n")
    else:
        # print("no circles")
        clock.tick()
        img = sensor.snapshot()
        predictions_list = list(zip(labels, net.predict([img])[0].flatten().tolist()))
        pred = ""
        pred_conf = -1
        for i in range(len(predictions_list)):
            if predictions_list[i][1]>pred_conf:
                pred = predictions_list[i][0]
                pred_conf = predictions_list[i][1]
        vcp.write(f"Letter:{pred}\n")

    time.sleep_ms(500)
