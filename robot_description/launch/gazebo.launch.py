import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg = get_package_share_directory('robot_description')
    urdf = xacro.process_file(os.path.join(pkg, 'urdf', 'robot.urdf.xacro')).toxml()

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-r empty.sdf'}.items())

    rsp = Node(package='robot_state_publisher', executable='robot_state_publisher',
               parameters=[{'robot_description': urdf, 'use_sim_time': True}])

    spawn = Node(package='ros_gz_sim', executable='create',
                 arguments=['-topic', 'robot_description', '-name', 'depo_robot', '-z', '0.05'])

    clock = Node(package='ros_gz_bridge', executable='parameter_bridge',
                 arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock', '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist', '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry', '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V', '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model'])

    return LaunchDescription([gazebo, rsp, spawn, clock])
