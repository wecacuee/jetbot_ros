import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir,LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    
    teleop_keyboard = Node(package='jetbot_ros', node_executable='teleop_keyboard',
                           prefix='xterm -e',
                           output='screen',
                           emulate_tty=True)              
      
    data_collection = Node(package='jetbot_ros', node_executable='data_collection',
                           parameters=[{"data_path": "/workspace/src/jetbot_ros/data/my_dataset"}],
                           output='screen', emulate_tty=True) 
                           
    return LaunchDescription([
        teleop_keyboard,
        data_collection
    ])