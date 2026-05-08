import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
    Node(
        package='imu_pkg',
        executable='imu_node',
        name='imu',
        output='screen',
        emulate_tty=True,
        # This will mute all INFO messages (called from get_logger().info("..."))
        arguments=['--ros-args','--log-level','WARN']
    ),
    Node(
        package='control_pkg',
        executable='control_node',
        name='control',
        output='screen',
        emulate_tty=True
    ),
    Node(
        package='led_pkg',
        executable='led_node',
        name='led',
        output='screen',
        emulate_tty=True,
        arguments=['--ros-args','--log-level','WARN']
    ),
    Node(
        package='led_pkg',
        executable='button_node',
        name='button',
        output='screen',
        emulate_tty=True,
        arguments=['--ros-args','--log-level','WARN']
    ),
    Node(
        package='motor_pkg',
        executable='motor_node',
        name='motor',
        output='screen',
        emulate_tty=True
    ),
    Node(
        package='openmv_pkg',
        executable='openmv_node',
        name='openmv',
        output='screen',
        emulate_tty=True,
        arguments=['--ros-args','--log-level','WARN']
    ),
])