import board
import time
import adafruit_tca9548a
import adafruit_tcs34725
i2c = board.I2C()
tca = adafruit_tca9548a.TCA9548A(i2c)
color = adafruit_tcs34725.TCS34725(tca[3])

def get():
#while True:
#    print("color: {0},{1},{2}".format(*color.color_rgb_bytes))
#    print("lux: {0}".format(color.lux))
#    time.sleep(1)

    return [color.color_raw, color.lux]

while True:
    c1=[]
    c2=[]
    c3=[]
    c4=[]
    lux=[]
    x=input("Calibrate color: ")
    for j in range(15):
        c1.append(get()[0][0])
        c2.append(get()[0][1])
        c3.append(get()[0][2])
        c4.append(get()[0][3])
        lux.append(get()[1])
        time.sleep(.1)
        print(j+1)
        print(get())
    print(f"{x} color range: ({min(c1)}-{max(c1)},{sum(c1)/15},{min(c2)}-{max(c2)},{sum(c2)/15},{min(c3)}-{max(c3)},{sum(c3)/15}, {min(c4)}-{max(c4)}), {sum(c4)/15},lux range: {min(lux)}-{max(lux)},{sum(lux)/15}")
'''
    if sum(c4)/15<5:
       	print("black")
    if 6<sum(c4)<10:
	print("red")
    if 
'''
