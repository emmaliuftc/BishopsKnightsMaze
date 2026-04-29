# Dataset Capture Script - By: student - Wed Apr 29 2026

# Use this script to control how your OpenMV Cam captures images for your dataset.
# You should apply the same image pre-processing steps you expect to run on images
# that you will feed to your model during run-time.

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # Modify as you like.
sensor.set_framesize(sensor.QVGA) # Modify as you like.
sensor.set_windowing((320,240))
sensor.skip_frames(time = 5000)

clock = time.clock()

for i in range(600):
    clock.tick()
    img = sensor.snapshot()
    # Apply lens correction if you need it.
    img.lens_corr()
    # Apply rotation correction if you need it.
    # img.rotation_corr()
    # Apply other filters...
    # E.g. mean/median/mode/midpoint/etc.
    print("\x1b[64OMV")
    # print(clock.fps())
    time.sleep(0.1)
