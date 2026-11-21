import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg = get_package_share_directory('robot_description')
    urdf = xacro.process_file(os.path.join(pkg, 'urdf', 'robot.urdf.xacro')).toxml()
    rviz = os.path.join(pkg, 'rviz', 'robot.rviz')

    return LaunchDescription([
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': urdf}]),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui'),
        Node(package='rviz2', executable='rviz2', arguments=['-d', rviz]),
    ])
