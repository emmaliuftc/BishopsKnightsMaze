import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool, Int32, Float64MultiArray
import time

class Control(Node):
    def __init__(self):
        super().__init__("control_node")
        
        # ------------- CONSTANTS (sort of)

        self.MOTOR_FORWARD = 0
        self.MOTOR_RAMP = 1
        self.MOTOR_STAIR = 2
        self.MOTOR_LEFT_TURN = 3
        self.MOTOR_RIGHT_TURN = 4
        self.MOTOR_BIG_TURN = 5
        self.MOTOR_IDLE = 6
        self.MOTOR_KIT = 7
        self.MOTOR_FORCE_STOP = 8
        # little debugging things
        self.MOTOR_STATES = [self.MOTOR_IDLE, self.MOTOR_KIT]
        self.motor_test = 0

        # ------------ CONTROL NODE VARIABLES

        self.motor_ready = True

        self.WAITING = 0
        self.ALGO = 1
        self.STOP = 2
        self.state = 0

        self.button_subscription = self.create_subscription(Bool, "button_topic", self.button_callback, 10)
        # self.openmv_subscription = self.create_subscription(Bool, )
        self.motor_status_sub = self.create_subscription(Bool, "motor_ready", self.status_callback, 10)

        self.led_publisher_ = self.create_publisher(Bool, "led_topic", 10)
        self.motor_publisher_ = self.create_publisher(Int32, "motor_topic",10)
        

        self.led_timer = self.create_timer(5, self.led_timer_callback)
        self.led_state = Bool()

    # ------------ INPUT HANDLERS

    def button_callback(self, msg):
        if msg.data:
            # Button is pressed -> Cycle forwards one state
            self.state = (self.state + 1) % 3
            self.get_logger().info("Button pressed") # Perhaps this is backwards let us lock in mayhaps

    def status_callback(self,msg):
        self.motor_ready = msg.data


    def master_loop(self):
        if not self.motor_status:
            return
        else:
            match self.state:
                case self.WAITING:
                    # Do nothing...?
                    return
                case self.ALGO:
                    # Begin algorithm
                    self.led_state.data = not self.led_state.data
                    self.led_publisher_.publish(self.led_state)
                    # self.get_logger().info(f"Publishing: {self.led_state} to led_topic")
                    
                    self.motor_test = (self.motor_test + 1) % (len(self.MOTOR_STATES))
                    self.msg = Int32()
                    self.msg.data = self.MOTOR_STATES[self.motor_test]
                    self.motor_publisher_.publish(self.msg)
                    self.get_logger().info(f"Publishing: {self.msg.data} to motor_topic")

                case self.STOP:
                    # Stop everything
                    self.get_logger().info("STOP EVERYTHING RAHHHHHHHHHH!!!!!!")
                    raise SystemExit





def main():
    rclpy.init()
    node = Control()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()