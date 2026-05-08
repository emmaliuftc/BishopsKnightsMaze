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
       
        # Make these match the actual ID numbers.  
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
    
        self.VELOCITY = 100
        self.RAMP_VELOCITY = 200
        self.STAIR_VELOCITY = 150

        self.TURN_ANGLE = 10
        self.turned = True

        self.encoder_timer = self.create_timer(0.1, self.encoder_timer_callback)

        self.motor_subscription = self.create_subscription(Int32, "motor_topic", self.motor_callback,10)
        self.encoder_publisher_ = self.create_publisher(Float64MultiArray, "encoder_topic", 10)

        self.gyro_subscription = self.create_subscription(Float64MultiArray, "gyro_topic", self.gyro_callback,10)


        self.kit_subscription = self.create_subscription(String, "kit_topic", self.kit_callback, 10)

    # def stop():
    #     drive(0)
    
    # def turn(vel, t=0):
    #     if t==0:
    #         self.packet_handler.write4ByteTxRx(port, self.MOTOR_LB, 104, vel)
    #         self.packet_handler.write4ByteTxRx(port, self.MOTOR_LF, 104, vel)
    #         self.packet_handler.write4ByteTxRx(port, self.MOTOR_RB, 104, vel)
    #         self.packet_handler.write4ByteTxRx(port, self.MOTOR_RF, 104, vel)
    #     else:
    #         turn(vel)
    #         time.sleep(t)
    #         stop()

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



    def drive(self, vel):
        self.get_logger().info(f"Driving at {vel}")
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LB, 104, vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LF, 104, vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RB, 104, -vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RF, 104, -vel)

    def turn(self, vel):
        self.get_logger().info(f"Turning at {vel}")
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LB, 104, vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LF, 104, vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RB, 104, vel)
        self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RF, 104, vel)

    def gyro_callback(self, msg):
        self.gyro_angle = msg.data
        self.get_logger().info(f"GYRO ANGLE: {self.gyro_angle}")



    def stop(self):
        self.drive(0)

    def encoder_timer_callback(self):
        msg = Float64MultiArray()
        positions = self.get_positions()
        # positions = []
        # pos,_,_ = self.packet_handler.read4ByteTxRx(self.port, self.MOTOR_LB, 132)
        # positions.append(round(pos,3))
        # pos,_,_ = self.packet_handler.read4ByteTxRx(self.port, self.MOTOR_LF, 132)
        # positions.append(round(pos,3))
        # pos,_,_ = self.packet_handler.read4ByteTxRx(self.port, self.MOTOR_RB, 132)
        # positions.append(round(pos,3))
        # pos,_,_ = self.packet_handler.read4ByteTxRx(self.port, self.MOTOR_RF, 132)
        # positions.append(round(pos,3))
        # pos,_,_ = self.packet_handler.read4ByteTxRx(self.port, self.GEAR, 132)
        # positions.append(round(pos,3))
        msg.data = [float(x) for x in positions]
        self.encoder_publisher_.publish(msg)
    
    def turned_to_target(self, target_angle)->bool:
        if self.angle >= target_angle:
            self.turned = True
            return True
        return False

    def motor_callback(self, msg):
        self.get_logger().info(f"Receiving: {msg.data}")
        match msg.data:
            case 0:
                # Drive forward one tile
                target_pos = self.get_positions()[1] + 3725
                self.get_logger().info(f"POSTION AT CALLBACK: {target_pos}")
                self.drive(self.VELOCITY)
                while self.get_positions()[1] < target_pos:
                    self.get_logger().info(f"CURRENT POSITION: {self.get_positions()[1]}")
                    # self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LB, 104, vel)
                    # self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LF, 104, vel)
                    # self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RB, 104, -vel)
                    # self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RF, 104, -vel)
                    # self.packet_handler.write4ByteTxRx(self.port, self.GEAR, 104, vel)
                    
                self.stop()
            case 1:
                # Drive forward one ramp
                target_pos = self.get_positions()[1] + 3725
                self.get_logger().info(f"POSTION AT CALLBACK: {target_pos}")
                self.drive(self.RAMP_VELOCITY)
                while self.get_positions()[1] < target_pos:
                    self.get_logger().info(f"CURRENT POSITION: {self.get_positions()[1]}")
                    # self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LB, 104, vel)
                    # self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_LF, 104, vel)
                    # self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RB, 104, -vel)
                    # self.packet_handler.write4ByteTxRx(self.port, self.MOTOR_RF, 104, -vel)
                    # self.packet_handler.write4ByteTxRx(self.port, self.GEAR, 104, vel)
                    
                self.stop()                
            case 2:
                # Drive forward one stair
                target_pos = self.get_positions()[1] + 3725
                self.get_logger().info(f"POSTION AT CALLBACK: {target_pos}")
                self.drive(self.STAIR_VELOCITY)
                while self.get_positions()[1] < target_pos:
                    self.get_logger().info(f"CURRENT POSITION: {self.get_positions()[1]}")
                self.stop()
            case 3:
                # Turn left
                self.turned = False
                target_ang = self.gyro_angle[2] + self.TURN_ANGLE
                self.turn(self.VELOCITY)
                if self.turned_to_target(target_ang)
                while self.gyro_angle[2] < target_ang:
                    self.get_logger().info(f"CURRENT ANGLE: {self.gyro_angle[2]}")
                self.stop()

            case 4:
                # Turn right
                target_ang = self.gyro_angle[2] - self.TURN_ANGLE
                self.turn(self.VELOCITY)
                while self.gyro_angle[2] > target_ang:
                    self.get_logger().info(f"CURRENT ANGLE: {self.gyro_angle[2]}")
                self.stop()
    
            case 5:
                # Turn 180
                target_ang = self.gyro_angle[2] - 2 * self.TURN_ANGLE # Maybe need to flip sign
                self.turn(self.VELOCITY)
                while self.gyro_angle[2] > target_ang: # Maybe need to flip sign
                    self.get_logger().info(f"CURRENT ANGLE: {self.gyro_angle[2]}")
                self.stop()

            case _:
                self.get_logger().info("Lets lock in.")

    def kit_callback(self, msg):
        # print("moving to zero)")
        # self.packet_handler.write4ByteTxRx(port, self.GEAR, 116, 0)
        # time.sleep(2)
        if msg.data == "drop":
            position, result, error = self.packet_handler.read4ByteTxRx(self.port, self.GEAR, 132)
            # print(position, result, error)
            # print("moving to pos+1/9")
            new_position = (position + 455)
            # kit_go_to_pos(new_position)
            self.packet_handler.write4ByteTxRx(self.port, self.GEAR, 116, new_position)



def main():
    rclpy.init()
    node = motor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()