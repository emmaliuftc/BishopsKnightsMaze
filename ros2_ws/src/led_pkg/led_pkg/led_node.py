import rclpy
from rclpy.node import Node
from gpiozero import LED
from gpiozero.pins.lgpio import LGPIOFactory
from std_msgs.msg import String, Bool



class Led(Node):
    def __init__(self):
        super().__init__("led_node")
        self.factory = LGPIOFactory(chip=14)
        self.led = LED(14, pin_factory=self.factory)

        self.publisher_ = self.create_publisher(String, "chatter", 10)
        self.led_subscription = self.create_subscription(Bool, "led_topic", self.led_callback, 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
    
    def timer_callback(self):
        # self.led.toggle()
        # state = "ON" if self.led.is_lit else "OFF"
        # msg = String()
        # msg.data = f"Leds going???? State: {state}"
        # self.get_logger().info(f"Publishing: {msg}")        
        # self.publisher_.publish(msg)
        ...
    
    def led_callback(self,msg):
        self.get_logger().info(f"I heard {msg} from led_topic")
        if msg.data:
            self.led.on()
        else:
            self.led.off()

def main():
    rclpy.init()
    node = Led()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()