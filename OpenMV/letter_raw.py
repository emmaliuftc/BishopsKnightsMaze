import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_windowing((240, 240))
clock = time.clock()

while True:
    img = sensor.snapshot()
    img.to_grayscale()
    blob = max(img.find_blobs([(0,15)], merge = True), key=lambda b:b.pixels())
    roi = img.copy(roi=blob.rect())
    img.draw_rectangle(blob.rect(),color=(255,0,0))
