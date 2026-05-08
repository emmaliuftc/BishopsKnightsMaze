import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import RegisterEventHandler, EmitEvent
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown

def generate_launch_description():
    control = Node(
        package='control_pkg',
        executable='control_node',
        name='control',
        output='screen',
        emulate_tty=True
    )
    imu = Node(
        package='imu_pkg',
        executable='imu_node',
        name='imu',
        output='screen',
        emulate_tty=True,
        # This will mute all INFO messages (called from get_logger().info("..."))
        arguments=['--ros-args','--log-level','WARN']
    )
    led = Node(
        package='led_pkg',
        executable='led_node',
        name='led',
        output='screen',
        emulate_tty=True,
        arguments=['--ros-args','--log-level','WARN']
    )
    button = Node(
        package='led_pkg',
        executable='button_node',
        name='button',
        output='screen',
        emulate_tty=True,
        arguments=['--ros-args','--log-level','WARN']
    )
    motors = Node(
        package='motor_pkg',
        executable='motor_node',
        name='motor',
        output='screen',
        emulate_tty=True
    )
    openmv = Node(
        package='openmv_pkg',
        executable='openmv_node',
        name='openmv',
        output='screen',
        emulate_tty=True,
        arguments=['--ros-args','--log-level','WARN']
    )

    shutdown_handler = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=control,
            on_exit=[
                EmitEvent(event=Shutdown(reason='Control node exited...'))
            ]
        )
    )

    return LaunchDescription([
        control, imu, led, button, motors, openmv, shutdown_handler
    ])