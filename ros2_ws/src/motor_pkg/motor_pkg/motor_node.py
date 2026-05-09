import rclpy
from rclpy.node import Node
from gpiozero import LED
from gpiozero.pins.lgpio import LGPIOFactory
from std_msgs.msg import String, Bool, Int32, Float64MultiArray
from dynamixel_sdk import *
import math

class motor(Node):
    def __init__(self):
        super().__init__("motor_node")
       
        # ------------- MOTOR SETUP
        
        self.MOTOR_LB = 1
        self.MOTOR_LF = 2
        self.MOTOR_RB = 3
        self.MOTOR_RF = 4
        self.GEAR = 5

        # If you have more/fewer than 4 motors make sure to adjust this list
        self.motors = [self.MOTOR_LB, self.MOTOR_LF, self.MOTOR_RB, self.MOTOR_RF, self.GEAR]
        self.tires = [self.MOTOR_LB, self.MOTOR_LF, self.MOTOR_RB, self.MOTOR_RF]

        # This identifies the USB port where the motor controller is attached
        self.port = PortHandler('/dev/ttyUSB0')
        # This object contains the methods for reading/writing
        self.packet_handler = PacketHandler(2.0)

        # SETUP

        # Start up both handlers
        # print("Opening USB port and establishing connect\n")
        self.port.openPort()
        self.port.setBaudRate(57600)

        # Read the ID numbers from the motor memory to test connection.
        # Count how many successes to make sure that all are successes.
        # print("Test reading from each motor:")
        read_success = 0
        while read_success < len(self.motors):
            for motor in self.motors:
                # ID is 1 byte, stored at memory address 7.
                motor_id, result, error = self.packet_handler.read1ByteTxRx(
                        self.port, motor, 7)
                if result != COMM_SUCCESS:
                    self.get_logger().info("Read result was not a success.  The SDK says:")
                    self.get_logger().info("error fix uer code")
                    # print("Read result was not a success.  The SDK says:")
                    # print(f"{self.packet_handler.getTxRxResult(result)}") 
                elif error != 0:
                    self.get_logger().info("error fix uer code")
                    # print("Error found in reading.  The SDK says:")
                    # print(f"{self.packet_handler.getRxPacketError(error)}")
                else:
                    self.get_logger().info("error fix uer code")
                    # print(f"Initial connection to motor {motor_id} successful.")
                    read_success += 1
            if read_success < len(self.motors):
                self.get_logger().info("Not all motors succeeded. Retrying in 1 second.")
                # print("Not all motors succeeded.  Retrying in 1 second.\n\n")
                time.sleep(1)

        # # Set operating mode to extended position
        self.packet_handler.write1ByteTxRx(self.port, self.GEAR, 64, 0)
        self.packet_handler.write1ByteTxRx(self.port, self.GEAR, 11, 4)
        self.packet_handler.write1ByteTxRx(self.port, self.GEAR, 64, 1)
        for tire in self.tires:
            self.packet_handler.write1ByteTxRx(self.port, tire, 64, 0)
            self.packet_handler.write1ByteTxRx(self.port, tire, 11, 1)
            self.packet_handler.write1ByteTxRx(self.port, tire, 64, 1)
        time.sleep(0.1)
    
        # ----------- CONSTANTS

        self.FORWARD = 0
        self.RAMP = 1
        self.STAIR = 2
        self.LEFT_TURN = 3
        self.RIGHT_TURN = 4
        self.BIG_TURN = 5
        self.IDLE = 6
        self.KIT = 7
        self.TWO_KITS = 9
        self.FORCE_STOP = 8

        self.VELOCITY = 100
        self.RAMP_VELOCITY = 200
        self.STAIR_VELOCITY = 150

        self.ONE_TILE = 3725
        self.NINETY = 30

        # ------------ MOTOR VARIABLES

        self.state = self.IDLE
        self.motor_ready = Bool()
        self.current_angle = 1.0
        self.target_angle = 0
        self.current_position = 0
        self.target_pos = 0
        self.kit_current = 0
        self.kit_target = 0

        # ------------- TIMERS PUBS AND SUBS

        self.create_timer(0.05, self.control_loop)

        self.motor_subscription = self.create_subscription(Int32, "motor_topic", self.motor_callback,10)
        self.motor_ready_pub = self.create_publisher(Bool, "motor_ready", 10)

        self.gyro_subscription = self.create_subscription(Float64MultiArray, "gyro_topic", self.gyro_callback,10)

    # ---------- INPUT HANDLERS

    def get_positions(self):
        positions = []
        pos,_,_ = self.packet_handler.read4ByteTxRx(self.port, self.MOTOR_LB, 132)
        positions.append(round(pos,3))
        pos,_,_ = self.packet_handler.read4ByteTxRx(self.port, self.MOTOR_LF, 132)
        positions.append(round(pos,3))
        pos,_,_ = self.packet_handler.read4ByteTxRx(self.port, self.MOTOR_RB, 132)
        positions.append(round(pos,3))
        pos,_,_ = self.packet_handler.read4ByteTxRx(self.port, self.MOTOR_RF, 132)
        positions.append(round(pos,3))
        return positions

    def gyro_callback(self, msg):
        self.current_angle = msg.data[2]
        self.current_position = self.get_positions()[2]
        # self.get_logger().info(f"GYRO ANGLE: {self.current_angle}")

    # --------- THINGS TO DO

    def drive(self, vel):
        # self.get_logger().info(f"Driving at {vel}")
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LB, 104, vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LF, 104, vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RB, 104, -vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RF, 104, -vel)

    def stop(self):
        self.drive(0)

    def turn(self, vel):
        # self.get_logger().info(f"Turning at {vel}")
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LB, 104, vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LF, 104, vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RB, 104, vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RF, 104, vel)


    # ---------- ADJUST STATE

    def motor_callback(self, msg):
        self.get_logger().info(f"Receiving: {msg.data}")
        if msg.data == self.FORCE_STOP:
            self.state = self.IDLE
            self.stop()
        else:
            if not motor_ready: # If I'm busy just ignore
                self.get_logger().info("Rejecting command cuz motors are busy... BUT THIS SHOULDNT HAPPEN HELLO????????????")
            else:
                match msg.data:
                    case self.FORWARD:
                        self.target_position = self.current_position + self.ONE_TILE
                        self.state = self.FORWARD
                        self.get_logger().info(f"State: Forward to {self.target_position}")
                    case self.RAMP:
                        self.state = self.RAMP
                    case self.STAIR:
                        self.state = self.STAIR
                    case self.LEFT_TURN:
                        self.target_angle = self.current_angle - self.NINETY
                        self.state = self.LEFT_TURN
                    case self.RIGHT_TURN:
                        self.target_angle = self.current_angle + self.NINETY
                        self.state = self.RIGHT_TURN
                        self.get_logger().info(f"State: Right turn to {self.target_angle}")
                    case self.BIG_TURN:
                        self.state = self.BIG_TURN
                    case self.IDLE:
                        self.state = self.IDLE
                    case self.KIT:
                        self.kit_current,_,_ = self.packet_handler.read4ByteTxRx(self.port, self.GEAR, 132)
                        self.kit_target = (self.kit_current + 455)
                        self.state = self.KIT
                    case self.TWO_KITS:
                        self.kit_current,_,_ = self.packet_handler.read4ByteTxRx(self.port, self.GEAR, 132)
                        self.kit_target = (self.kit_current + 2*455)
                        self.state = self.TWO_KITS

    # ---------- CHECKING EVERY TICK FOR ACTIVE STATE

    def control_loop(self):
        if self.state == self.IDLE:
            self.stop()
            self.get_logger().info("Idle")
            self.motor_ready.data =  True # Motor is ready to do other stuff
            self.motor_ready_pub.publish(self.motor_ready)            
        else:
            self.motor_ready.data = False # Motor is preoccupied
            self.motor_ready_pub.publish(motor_ready)
            match self.state:
                case self.FORWARD:
                    self.get_logger().info("Forward")
                    error = self.target_position - self.get_positions()[2]
                    if error < 10:
                        self.get_logger().info("Target forward reached")
                        self.state = self.IDLE
                    else:
                        self.drive(self.VELOCITY)
                case self.RIGHT_TURN:
                    self.get_logger().info("Right Turn")
                    error = self.target_angle - self.current_angle
                    if error < 2:
                        self.get_logger().info("Target right turn reached")
                        self.state = self.IDLE
                    else:
                        self.turn(self.VELOCITY)
                case self.KIT:
                    self.get_logger().info("Kit")
                    if self.kit_current != self.kit_target:
                        self.packet_handler.write4ByteTxRx(self.port, self.GEAR, 116, self.kit_target)
                    else:
                        self.get_logger().info("Dropping 1 kit")
                        self.state = self.IDLE
                case self.TWO_KITS:
                    self.get_logger().info("Two kits")
                    if self.kit_current != self.kit_target:
                        self.packet_handler.write4ByteTxRx(self.port, self.GEAR, 116, self.kit_target)
                    else:
                        self.get_logger().info("Dropping 2 kits")
                        self.state = self.IDLE
                case _:
                    self.get_logger().info("Ur a friggin brick brah")
    
    def destroy_node(self):
        self.stop()
        super().destroy_node()
        
def main():
    rclpy.init()
    node = motor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()