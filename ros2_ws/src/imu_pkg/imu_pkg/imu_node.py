import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64MultiArray
import time
import busio
import board
import adafruit_tca9548a
import math
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
)
from adafruit_bno08x.i2c import BNO08X_I2C
import adafruit_vl53l0x
import adafruit_tcs34725

class imu(Node):
    def __init__(self):
        super().__init__("imu_node")
    
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # 100000 ?
        self.tca = adafruit_tca9548a.TCA9548A(self.i2c)

        for channel in range(8):
            if self.tca[channel].try_lock():
                # self.get_logger().info("Channel {}:".format(channel), end="")
                addresses = self.tca[channel].scan()
                # self.get_logger().info([hex(address) for address in addresses if address != 0x70])
                self.tca[channel].unlock()

        self.bno = BNO08X_I2C(self.tca[6])
        self.bno.enable_feature(BNO_REPORT_ACCELEROMETER)
        self.bno.enable_feature(BNO_REPORT_GYROSCOPE)
        self.bno.enable_feature(BNO_REPORT_MAGNETOMETER)
        self.bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
        

        self.vlleft = adafruit_vl53l0x.VL53L0X(self.tca[2])
        self.vlfront = adafruit_vl53l0x.VL53L0X(self.tca[3])
        self.vlright = adafruit_vl53l0x.VL53L0X(self.tca[4])

        self.color = adafruit_tcs34725.TCS34725(self.tca[5])

        self.publisher_ = self.create_publisher(String, "imu_topic",10)
        self.gyro_publisher_ = self.create_publisher(Float64MultiArray, "gyro_topic",10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        start_time = time.time()
        angle = [0, 0, 0]
        while True:
            gyro_x, gyro_y, gyro_z = self.bno.gyro
            gyro = [gyro_x, gyro_y, gyro_z]
            dt = time.time() - start_time
            dg = [g * dt * 180 / math.pi for g in gyro] # 
            angle = [x+y for x, y in zip(dg,angle)]
            msg = Float64MultiArray()
            msg.data = angle       
            self.gyro_publisher_.publish(msg)
            start_time = time.time()
            


    def timer_callback(self):
        accel_x, accel_y, accel_z = self.bno.acceleration
        
        dist_l = self.vlleft.range
        dist_f = self.vlfront.range
        dist_r = self.vlright.range

        r, g, b, c = self.color.color_raw

        # Can use ColorRGBA() perhaps?
        # Maybe do some extra processing here
        # Check screenshots

        msg = String()
        msg.data = f"{accel_x}, {accel_y}, {accel_z}, DIST LEFT: {dist_l}, FRONT: {dist_f} RIGHT: {dist_r}, colors: {r}, {g}, {b}, {c}"
        
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing: imu data")


        

def main():
    rclpy.init()
    node = imu()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()