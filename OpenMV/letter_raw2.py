import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_windowing((240, 240))
clock = time.clock()

phi = image.Image("phi-_1_.pgm")
#print(phi.size())
#@print(phi.width(), phi.height())
#psi = image.Image("psi.pgm").resize(*SIZE)
#omega = image.Image("omega.pgm").resize(*SIZE)

def score(a,b):
    good = 0
    if not x_scale or not y_scale:
        return 0
    for y in range(x_scale-1):
        for x in range(y_scale-1):
            if a.get_pixel(x,y) and b.get_pixel(x,y):
                #print(f"SCALE: {x_scale},{y_scale}")
                #print(f"x, y = {x},{y}")
                diff = abs(a.get_pixel(x,y)/max_b - b.get_pixel(x,y)/255)*100
                # print(f"{x=} {y=} {max_b=} {a.get_pixel(x,y)/max_b*100=} {b.get_pixel(x,y)/2.55=}  {diff=} {(diff < 50)=}")

                if diff < 50:
                    good += 1
    print(good, x_scale, y_scale)
    print(good/(x_scale*y_scale)*100)
    return good/x_scale/y_scale*100

if True:
    img = sensor.snapshot().to_grayscale()
    blobs = img.find_blobs([(0,35)], merge = True)
    time.sleep(0.1)
    if blobs:
        blob = max(blobs, key=lambda b:b.pixels())
        roi = img.copy(roi=blob.rect())
        # img.draw_rectangle(*blob.rect(), thickness=5)
        sensor.flush()
        print(roi)
        stats = roi.get_statistics()
        max_b = stats.max()
        print(max_b)
        try:
            if roi.width() > phi.width():
                roi = roi.scale(x_scale = phi.width()/roi.width(), y_scale=phi.height()/roi.height())
                x_scale = roi.width()
                y_scale = roi.height()
            else:
                phi = phi.scale(x_scale = roi.width()/phi.width(), y_scale=roi.height()/phi.height())
                x_scale = phi.width()
                y_scale = phi.height()
        except OSError as e:
            print(e)
    else:
        print("No ROI")
    s_phi= score(roi, phi)
    #s_psi = score(roi, psi)
    #s_omega= score(roi, omega)



