
import sensor, time, math
from pyb import LED
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
clock = time.clock()
THRESHOLD = (0, 25)

def vertical_histogram(img):
    hist = []
    for x in range(img.width()):
        total = 0
        for y in range(img.height()):
            # black pixel
            if img.get_pixel(x, y) < 50:
                total += 1
        hist.append(total)
    return hist


def count_peaks(hist, threshold=8):
    peaks = 0
    in_peak = False
    for v in hist:
        if v > threshold:
            if not in_peak:
                peaks += 1
                in_peak = True
        else:
            in_peak = False
    return peaks


def center_line_strength(img):
    x = img.width() // 2
    count = 0
    for y in range(img.height()):
        if img.get_pixel(x, y) < 50:
            count += 1
    return count


def bottom_occupancy(img):
    total = 0
    start_y = img.height() - 5
    for y in range(start_y, img.height()):
        for x in range(img.width()):
            if img.get_pixel(x, y) < 50:
                total += 1
    return total


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


def target_sense(img):
    img.lens_corr()
    # sensor.flush()
    # detect dark blobs

    circles = img.find_circles(threshold = 5000, x_margin = 0, y_margin = 0) # Supposed to be find_circles or something
    # circles = img.find_blobs([(0, 80, -50, 50, -50, 50)])

    if circles:
        # ellipse = image.get_enclosed_ellipse(circles)
        # print(len(circles), circles)
        lar_c = max(circles, key=lambda c:c.r())
        radius = lar_c.r()/5
        rings = [[] for _ in range(5)]
        # img.draw_circle(lar_c.x(), lar_c.y(), lar_c.r(), color = 255)
        sensor.flush()
        for i in range(5):
            ring = i+1
          #  print(f'ring{ring}')
            temp_radius = i*radius + radius/2
            for j in range(30):
                angle = math.pi/15*j
                pixel_loc = (lar_c.x() + int(temp_radius*math.cos(angle)), lar_c.y() + int(temp_radius*math.sin(angle)))
                pixel_rgb = img.get_pixel(pixel_loc[0], pixel_loc[1])
                # print(pixel_rgb)
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
        return "nothing"

LED(3).toggle()
time.sleep(3)
LED(3).toggle()


while True:

    img = sensor.snapshot()
    img.lens_corr()
    blobs = img.find_blobs([(40,70, -15, 10, 15, 45),(25, 50, -8, 10, -40, -20),(10,30,15,40,5,25),(15,40,-25,-10,-10,20)], area_threshold=20) # YBCG

    if blobs:
        likely = target_sense(img)
    else:
        img = sensor.snapshot()
        img = img.to_grayscale()
        blobs = img.find_blobs([(0,40)], merge = True, area_threshold = 1000)
        # time.sleep(0.1)
        if blobs:
            blob = max(blobs, key=lambda b:b.pixels())
            roi = img.copy(roi=blob.rect())
            # img.draw_rectangle(*blob.rect(), thickness=3)
            hist = vertical_histogram(roi)
            peaks = count_peaks(hist)
            center_strength = center_line_strength(roi)
            bottom = bottom_occupancy(roi)
            aspect = blob.w() / blob.h()


            phi_score = 0
            psi_score = 0
            omega_score = 0

            # ---- PHI ----

            if center_strength > 25:
                phi_score += 3

            if peaks == 1:
                phi_score += 2

            # ---- PSI ----

            if peaks >= 3:
                psi_score += 4

            if center_strength > 15:
                psi_score += 1

            # ---- OMEGA ----

            if aspect > 1.2:
                omega_score += 3

            if bottom < 40:
                omega_score += 3

            if peaks == 2:
                omega_score += 2

            # =====================
            # Classification
            # =====================

            scores = {
                "PHI": phi_score,
                "PSI": psi_score,
                "OMEGA": omega_score
            }

            symbol = max(scores, key=scores.get)

            # =====================
            # Display
            # =====================

    #         print("--------------------------------")
    #         print("Peaks:", peaks)
    #         print("Center:", center_strength)
    #         print("Bottom:", bottom)
    #         print("Aspect:", aspect)

    #         print("PHI:", phi_score)
    #         print("PSI:", psi_score)
    #         print("OMEGA:", omega_score)

    #         print("Detected:", symbol)

            likely = symbol

            # img.draw_string(
            #     blob.x(),
            #     blob.y() - 10,
            #     symbol,
            #     color=255
            # )
        else:
            likely = "nothing"

    print(likely)
    time.sleep(0.5)

