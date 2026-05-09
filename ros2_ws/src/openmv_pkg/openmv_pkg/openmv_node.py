import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
import serial

class openmv(Node):
    def __init__(self):
        super().__init__("openmv_node")
        
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
            self.get_logger().info("Successfully connected to can on /dev/ttyACM0")
        except Exception as e:
            try:
                self.ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
                self.get_logger().info("Successfully connected to can on /dev/ttyACM1")
            except Exception as e:
                self.get_logger().info(f"Failed to connect to cam: {e}")
                return

        self.publisher_ = self.create_publisher(String, 'openmv_data', 10)
        self.timer = self.create_timer(0.05, self.timer_callback)
        
    def timer_callback(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').strip()
            # result = line.split(":")
            # if result[0]=="Target":
            #     # its taget
            # else: # It's a letter

            msg = String()
            msg.data = line
            # Publishing everything that the camera is seeing (the logic is in the OpenMV code)
            self.publisher_.publish(msg)
            self.get_logger().info(f"Received: '{line}'")

def main():
    rclpy.init()
    node = openmv()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()