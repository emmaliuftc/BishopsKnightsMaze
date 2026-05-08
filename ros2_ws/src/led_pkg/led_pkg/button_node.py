import rclpy
from rclpy.node import Node
from gpiozero import Button as gpiobutton
from gpiozero.pins.lgpio import LGPIOFactory
from std_msgs.msg import String, Bool

class button(Node):
    def __init__(self):
        super().__init__("button_node")
        self.factory = LGPIOFactory(chip=14)
        self.button = gpiobutton(17, pin_factory=self.factory)

        self.button_publisher_ = self.create_publisher(Bool, "button_topic", 10)
        while True:
            msg = Bool()
            msg.data = self.button.is_active
            self.button_publisher_.publish(msg)

def main():
    rclpy.init()
    node = button()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()