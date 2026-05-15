import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_windowing((240, 240))
clock = time.clock()

v_list=[]
c_list=[]
center_list=[]
aspect_list=[]
bottom_list=[]
area_list=[]
density_list=[]
edge_list=[]
perim_list=[]
hline_list=[]

start=time.ticks_ms()

def vertical_line_count(lines):
    count = 0
    for l in lines:
        theta = l.theta()
        if theta < 15 or theta > 165:
            count += 1
    return count

def horizontal_line_count(lines):
    count = 0
    for l in lines:
        theta = l.theta()
        if 75 < theta < 105:
            count += 1
    return count

def center_occupancy(img, roi):
    x, y, w, h = roi
    stats = img.get_statistics(roi=(x + w//3, y + h//3, w//3, h//3))
    return stats.mean()

def bottom_opening(img, roi):
    x, y, w, h = roi
    open_pixels = 0
    for px in range(x + w//4, x + 3*w//4):
        if img.get_pixel(px, y + h - 5) > 100:
            open_pixels += 1
    return open_pixels

while True:
    clock.tick()
    img = sensor.snapshot()
    img.binary([(0, 90)])

    blobs = img.find_blobs([(0, 50)], pixels_threshold=1000, area_threshold=1000, merge=True)

    for b in blobs:
        roi = b.rect()
        x, y, w, h = roi

        lines = img.find_lines(roi=roi, threshold=1200)
        v_lines = vertical_line_count(lines)
        h_lines = horizontal_line_count(lines)

        circles = img.find_circles(roi=roi, threshold=2500, r_min=5, r_max=40)
        num_circles = len(circles)

        center_fill = center_occupancy(img, roi)
        aspect_ratio = w / h
        bottom_gap = bottom_opening(img, roi)

        # NEW FEATURE 1: area
        area = b.area()

        # NEW FEATURE 2: density
        density = b.density()

        # NEW FEATURE 3: edge count (approx)
        edges = img.find_edges(image.EDGE_CANNY, roi=roi)
        edge_stats = edges.get_statistics().mean()

        # NEW FEATURE 4: perimeter estimate
        perim = 2 * (w + h)

        # STORE VALUES
        v_list.append(v_lines)
        c_list.append(num_circles)
        center_list.append(center_fill)
        aspect_list.append(aspect_ratio)
        bottom_list.append(bottom_gap)

        area_list.append(area)
        density_list.append(density)
        edge_list.append(edge_stats)
        perim_list.append(perim)
        hline_list.append(h_lines)

        avg1= sum(v_list)/len(v_list)
        avg2= round(sum(c_list)/len(c_list),2)
        avg3= sum(center_list)/len(center_list)
        avg4= round(sum(aspect_list)/len(aspect_list),2)
        avg5= round(sum(bottom_list)/len(bottom_list),2)
        avg6= round(sum(area_list)/len(area_list),2)
        avg7= round(sum(density_list)/len(density_list),2)
        avg8= round(sum(edge_list)/len(edge_list),2)
        avg9= round(sum(perim_list)/len(perim_list),2)
        avg10= round(sum(hline_list)/len(hline_list),2)
        print(avg1, avg2, avg3, avg4, avg5, avg6, avg7, avg8, avg9, avg10)

