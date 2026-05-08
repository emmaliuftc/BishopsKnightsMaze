import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool, Int32, Float64MultiArray
import time

class Control(Node):
    def __init__(self):
        super().__init__("control_node")
                
        
        self.MOTOR_STATES = [0,7]
        self.motor_test = 0
        self.motor_ready = True

        self.WAITING = 0
        self.ALGO = 1
        self.STOP = 2
        self.state = 0

        self.button_subscription = self.create_subscription(Bool, "button_topic", self.button_callback, 10)
        # self.openmv_subscription = self.create_subscription(Bool, )

        self.led_publisher_ = self.create_publisher(Bool, "led_topic", 10)
        self.motor_publisher_ = self.create_publisher(Int32, "motor_topic",10)
        

        self.led_timer = self.create_timer(5, self.led_timer_callback)
        self.led_state = Bool()


    def button_callback(self, msg):
        if msg.data:
            # Button is pressed -> Cycle forwards one state
            self.state = self.state + 1
            self.get_logger().info("Button pressed")

    def led_timer_callback(self):
        
        # # self.get_logger().info(f"I heard {msg} from chatter")
        # self.led_state.data = not self.led_state.data
        # self.led_publisher_.publish(self.led_state)
        # # self.get_logger().info(f"Publishing: {self.led_state} to led_topic")
        
        # self.motor_test = (self.motor_test + 1) % (len(self.MOTOR_STATES))
        # self.msg = Int32()
        # self.msg.data = self.MOTOR_STATES[self.motor_test]
        # self.motor_publisher_.publish(self.msg)
        # self.get_logger().info(f"Publishing: {self.msg.data} to motor_topic")
        
        # # msg = String()
        # # msg.data = "drop"
        # # self.kit_publisher_.publish(msg)
        # # self.get_logger().info(f"Publishing: {msg} to kit_topic")
        
        
        ...





def main():
    rclpy.init()
    node = Control()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()