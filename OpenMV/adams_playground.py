# set up + open camera
import sensor
import math
import time
from pyb import Servo


sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QVGA) # medium resolution
sensor.skip_frames(time=2000) # allow camera to adjust

letter = "undetected"
longest = 0
second_longest = 0
longest_line = None
second_longest_line = None

'''
s1 = Servo(1)
s2 = Servo(2)

s1.angle(90)
while True:
    s2.angle(0)
    time.sleep(1)
    s2.angle(90)
    time.sleep(1)
'''
colors = {"Yellow": (148, 134, 58),"Red":(82, 12, 16),"Blue":(16, 57, 115),"Green":(0, 36, 16),"Black":(0,8,0)}
list_of_color_names = ["Yellow", "Red", "Blue", "Green", "Black"]
list_of_color_rgb_tuples = [(148, 134, 58), (82, 12, 16), (16, 57, 115), (0, 36, 16), (0,8,0)]

def mode(data):
    counts = {}
    for x in data:
        counts[x] = counts.get(x,0) + 1
    max_count = max(counts.values())
    modes = []
    for x in counts:
        if counts[x] == max_count:
            modes.append(x)
    return modes

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

img = sensor.snapshot()
img.lens_corr()
sensor.flush()
# detect dark blobs

slices = 9

src_points = [(50, 40), (260,30),(300,200),(20,210)]
dst_points = [(0,0),(320,0),(320,240),(0,240)]

circles = img.find_circles(threshold = 5000, x_margin = 0, y_margin = 0)
while True:
    blobs = img.find_blobs([(0,100,-120,120,7,50)], pixels_threshold=30, merge=True)
  #  print(len(blobs),blobs)
    # for lb in blobs:
    lb = max(blobs, key=lambda b: b.area())
    img.draw_rectangle(lb.rect(), color=(255,0,0))
    img.draw_edges(lb.min_corners(), color=(0,255,0))
    # img.rotation_corr
    print(lb.min_corners())
    c = lb.min_corners()
    if c[0][1]-c[1][1]!=0:
        zrot = 90+math.atan((c[0][0]-c[1][0])/c[0][1]-c[1][1])*180/math.pi
    else:
        zrot = 0
    print(zrot)
    img = sensor.snapshot()
    time.sleep(1)
    img.rotation_corr(z_rotation=zrot)
    img = sensor.snapshot()
    time.sleep(1)
'''
if circles:
    print(len(circles), circles)
    lar_c = max(circles, key=lambda c:c.r())
    radius = lar_c.r()/5
    rings = [[] for _ in range(5)]
    img.draw_circle(lar_c.x(), lar_c.y(), lar_c.r(), color = 255)
    sensor.flush()
    for i in range(5):
        ring = i+1
        print(f'ring{ring}')
        temp_radius = i*radius + radius/2
        for j in range(slices):
            angle = 2*math.pi/slices*j
            pixel_loc = (lar_c.x() + int(temp_radius*math.cos(angle)), lar_c.y() + int(temp_radius*math.sin(angle)))
            pixel_rgb = img.get_pixel(pixel_loc[0], pixel_loc[1])
            pixel_color = closest_color(pixel_rgb[0], pixel_rgb[1], pixel_rgb[2])
            print(f"pixel:{pixel_loc}, color:{pixel_color}")
            img.draw_cross(pixel_loc[0], pixel_loc[1], tuple(255 - x for x in colors[pixel_color]), size=2)
            rings[i].append(pixel_color)
        sensor.flush()
    time.sleep(2)
    print(rings)
    for r in rings:
        print(mode(r))
    sensor.flush()
else:
    print("no circles")
'''
