import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # Modify as you like.
sensor.set_framesize(sensor.QVGA) # Modify as you like.
sensor.set_windowing((320,240))
sensor.skip_frames(time = 5000)

clock = time.clock()
clock.tick()
img = sensor.snapshot()
while True:
    img = sensor.snapshot()
