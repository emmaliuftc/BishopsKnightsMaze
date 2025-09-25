import time
import board
import adafruit_tca9548a
import adafruit_vl53l0x

i2c = board.I2C()
tca = adafruit_tca9548a.TCA9548A(i2c)

vl0 = adafruit_vl53l0x.VL53L0X(tca[0])
vl1 = adafruit_vl53l0x.VL53L0X(tca[1])
vl2 = adafruit_vl53l0x.VL53L0X(tca[2])
print("Lets goooo setup is done")


while True:
    print(f"Sensor 0: {vl0.distance}, Sensor 1: {vl1.distance}, Sensor 2: {vl2.distance}")
    time.sleep(0.5)
