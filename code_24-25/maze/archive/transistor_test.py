import time
import busio
import adafruit_vl53l0x
import board
import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

'''
p = GPIO.PWM(12, 1000)
	
# change speed (0.0 to 100.0)
p.start(100)
'''
	
GPIO.output(15, GPIO.HIGH)
GPIO.output(18, GPIO.LOW)
GPIO.output(23, GPIO.LOW)
GPIO.output(24, GPIO.LOW)

i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

time.sleep(1.0)
pin = 15
for i in range(10):
	if pin == 24:
		GPIO.output(15, GPIO.LOW)
		GPIO.output(24, GPIO.HIGH)
	elif pin == 15:
		GPIO.output(15, GPIO.HIGH)
		GPIO.output(24, GPIO.LOW)
	vl53 = adafruit_vl53l0x.VL53L0X(i2c)
	print(f"Range: {vl53.range}mm, pin {pin}")
	time.sleep(1.0)
	#if pin == 24:
	#	pin = 15
	#elif pin == 15:
	#	pin = 24

'''
pin_nums = [15, 18, 23, 24]
for pin in pin_nums: 
	GPIO.output(15, GPIO.LOW)
	GPIO.output(18, GPIO.LOW)
	GPIO.output(23, GPIO.LOW)
	GPIO.output(24, GPIO.LOW)
		
	# turn pin on
	GPIO.output(pin, GPIO.HIGH)
	
	i2c = busio.I2C(board.SCL, board.SDA)
	vl53 = adafruit_vl53l0x.VL53L0X(i2c)

	print(f"pin {pin} is on now...")
	time.sleep(1.0)
	for i in range(5):
		vl53 = adafruit_vl53l0x.VL53L0X(i2c)
		print("Range: {0}mm".format(vl53.range))
		time.sleep(1.0)
    
   '''
