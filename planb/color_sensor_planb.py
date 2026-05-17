import busio
import board
import adafruit_tca9548a
import math
import adafruit_tcs34725

list_of_color_names = ["Red", "Blue", "Black", "Silver", "White"]
list_of_color_tuples = [(125, 8, 8, 124), (2, 16, 16, 103), (45, 0, 0, 17), (25, 12, 12, 285), (13, 13, 6, 414)]
def closest_color(r,g, b, l=0):
    closest_color_diff = 1000000
    closest_color_name = "Unknown"
    for i in range(len(list_of_color_tuples)):
        red_diff = r - list_of_color_tuples[i][0]
        green_diff = g - list_of_color_tuples[i][1]
        blue_diff = b - list_of_color_tuples[i][2]
        l_diff = l - list_of_color_tuples[i][3]
        diff = math.sqrt((red_diff**2)+(green_diff**2)+(blue_diff**2)+((l_diff/20)**2))
        if diff < closest_color_diff:
            closest_color_diff =  diff
            closest_color_name = list_of_color_names[i]
    return closest_color_name


def setup():
    i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)  # 100000 ?
    tca = adafruit_tca9548a.TCA9548A(i2c)

    if tca[5].try_lock():
        # addresses = tca[channel].scan()
        tca[5].unlock()

    color = adafruit_tcs34725.TCS34725(tca[5])
    return color

def get_color(sensor):   
    return "White"     
    r, g, b = sensor.color_rgb_bytes
    l = sensor.lux
    color = closest_color(r, g, b, l)
    return color

def calibrate(sensor):
    cs = []
    for c in list_of_color_names:
        x = input(c)
        r, g, b = sensor.color_rgb_bytes
        l = int(sensor.lux)
        cs.append((r,g,b,l))
        print(r,g,b,l)
    print(cs)
# s = setup()
# calibrate(s)
# while True:
#     print(get_color(s))