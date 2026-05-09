
import sensor, image, time, uos

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # Modify as you like.
sensor.set_framesize(sensor.QVGA) # Modify as you like.
sensor.set_windowing((320,240))
sensor.skip_frames(time = 5000)

clock = time.clock()
folder = "frameys"
try:
    uos.mkdir(folder)
except:
    pass

for i in range(600):
    clock.tick()
    img = sensor.snapshot()
    # Apply lens correction if you need it.
    img.lens_corr()
    # Apply rotation correction if you need it.
    # img.rotation_corr()
    # Apply other filters...
    # E.g. mean/median/mode/midpoint/etc.
    # print("\x1b[64OMV")
    #saves it in folder/00i
    filename = folder + "/" + str(i) + ".jpg"
    img.save(filename)
    # print(clock.fps())
    time.sleep(0.1)
    print(f"Saved: {filename}")
