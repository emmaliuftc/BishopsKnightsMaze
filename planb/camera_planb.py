import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
import serial

def get_data():
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        print("Successfully connected to can on /dev/ttyACM0")
    except Exception as e:
        try:
            ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
            print("Successfully connected to can on /dev/ttyACM1")
        except Exception as e:
            print(f"Failed to connect to cam: {e}")
            return
    line = ser.readline().decode('utf-8').strip()
    return line