import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool, Int32, Float64MultiArray
import time

class Control(Node):
    def __init__(self):
        super().__init__("control_node")
        
        self.imu_subscription = self.create_subscription(String, "imu_topic", self.imu_callback, 10)
        
        self.led_publisher_ = self.create_publisher(Bool, "led_topic", 10)
        self.motor_publisher_ = self.create_publisher(Int32, "motor_topic",10)
        
        # self.encoder_subscription = self.create_subscription(Float64MultiArray, "encoder_topic", self.encoder_callback,10)

        self.kit_publisher_ = self.create_publisher(String, "kit_topic", 10)        

        self.led_timer = self.create_timer(5, self.led_timer_callback)
        self.led_state = Bool()

        self.motor_vel = Int32()
        self.motor_vel.data = 0

        self.STATES = [0,4,6]
        self.test = 0

    def imu_callback(self,msg):
        ...
        # self.get_logger().info(f"I heard {msg} from imu_topic")
    
    def encoder_callback(self,msg):
        ...
        # self.get_logger().info(f"I heard {msg} from encoder_topic")
    
    def led_timer_callback(self):
        # self.get_logger().info(f"I heard {msg} from chatter")
        self.led_state.data = not self.led_state.data
        self.led_publisher_.publish(self.led_state)
        # self.get_logger().info(f"Publishing: {self.led_state} to led_topic")
        
        self.test = (self.test + 1) % 3
        self.motor_vel.data = self.STATES[self.test]
        self.motor_publisher_.publish(self.motor_vel)
        self.get_logger().info(f"Publishing: {self.motor_vel.data} to motor_topic")
        

        '''
        COME BACK AND GIVE KIT A SEPARATE NODE..... PLEASEEEEEEEKKKKKKKK
        '''
        # msg = String()
        # msg.data = "drop"
        # self.kit_publisher_.publish(msg)
        # self.get_logger().info(f"Publishing: {msg} to kit_topic")





def main():
    rclpy.init()
    node = Control()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()