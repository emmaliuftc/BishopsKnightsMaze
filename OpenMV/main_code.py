# Edge Impulse - OpenMV Image Classification Example
#
# This work is licensed under the MIT license.
# Copyright (c) 2013-2024 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE

import sensor, time, ml, uos, gc, math

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

net = None
labels = None




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

def letter_sense():
    clock.tick()

    img = sensor.snapshot()

    predictions_list = list(zip(labels, net.predict([img])[0].flatten().tolist()))

   # for i in range(len(predictions_list)):
     #   print("%s = %f" % (predictions_list[i][0], predictions_list[i][1]))
    print(predictions_list)
    return predictions_list


colors = {"Yellow": (148, 134, 58),"Red":(82, 12, 16),"Blue":(16, 57, 115),"Green":(0, 36, 16),"Black":(0,8,0)}
list_of_color_names = [0, -1, 2, 1, -2] # ["Yellow", "Red", "Blue", "Green", "Black"]
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

def mode(lst):
    counts = {}

    for item in lst:
        counts[item] = counts.get(item, 0) + 1

    most_common = max(counts, key=counts.get)
    return most_common


def target_sense():

    img = sensor.snapshot()
    img.lens_corr()
    sensor.flush()
    # detect dark blobs

    circles = img.find_circles(threshold = 5000, x_margin = 0, y_margin = 0)
    if circles:
        # print(len(circles), circles)
        lar_c = max(circles, key=lambda c:c.r())
        radius = lar_c.r()/5
        rings = [[] for _ in range(5)]
        img.draw_circle(lar_c.x(), lar_c.y(), lar_c.r(), color = 255)
        sensor.flush()
        for i in range(5):
            ring = i+1
          #  print(f'ring{ring}')
            temp_radius = i*radius + radius/2
            for j in range(30):
                angle = math.pi/15*j
                pixel_loc = (lar_c.x() + int(temp_radius*math.cos(angle)), lar_c.y() + int(temp_radius*math.sin(angle)))
                pixel_rgb = img.get_pixel(pixel_loc[0], pixel_loc[1])
                pixel_color = closest_color(pixel_rgb[0], pixel_rgb[1], pixel_rgb[2])
                # print(f"pixel:{pixel_loc}, color:{pixel_color}")
                # img.draw_cross(pixel_loc[0], pixel_loc[1], tuple(255 - x for x in colors[pixel_color]), size=2)
                rings[i].append(pixel_color)
            sensor.flush()
        sensor.flush()
        ring_colors = []
        for ring in rings:
            ring_colors.append(mode(ring))
        print(ring_colors)
        return sum(ring_colors)
    else:
        return -99

while True:
    img = sensor.snapshot()
    blobs = img.find_blobs([(72,81,-12,2,25,46),(31,43,0,15,-52,-36),(31,45,28,43,1,24),(21,45,-23,-4,-6,11)], area_threshold=20)
    if blobs:
        likely = target_sense()
    else:
        letters = letter_sense()
        highest_confidence = 0
        likely = -99
        for l in letters:
            if l[1] > highest_confidence:
                if l[0] == "psi":
                    likely = 1
                elif l[0] == "phi":
                    likely = 2
                elif l[0] == "omega":
                    likely = 0
    print(likely)
    time.sleep(0.3)
