import time
import RPi.GPIO as GPIO



# Set up GPIO
GPIO.setmode(GPIO.BCM)
def time_light_on():
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.setup(17, GPIO.IN)
    start = time.perf_counter()

    while GPIO.input(17):
        time.sleep(0.000001)
    result = int((time.perf_counter() - start ) * 10E6)
    return result
 

while True:
    print(time_light_on())
    time.sleep(1)
    



'''
#set up sensors with each SENSOR_PIN 
def read_sensor(pin):
    GPIO.setup(pin, GPIO.IN)
    start_time = time.time()
    while GPIO.input(pin) == GPIO.HIGH:
        if time.time() - start_time > 0.01:
            return 10000  # Timeout for dark surfaces
    return time.time() - start_time

def identify_color():
    readings = [read_sensor(pin) for pin in SENSOR_PINS]
    #averaging the readings if there's multiple colors 
    avg_reading = sum(readings) / len(readings)
    print("Average Reading", avg_reading) 
    if avg_reading < 0.001:
        return "Black"
    elif avg_reading > 0.005:
        return "Silver"
    elif 0.002 < avg_reading < 0.004:
        return "Possible Color Surface"
    else:
        return "Unknown"

try:
    while True:
        detected_color = identify_color()
        print("Detected Surface:", detected_color)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
'''
