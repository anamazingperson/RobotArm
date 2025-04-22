from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Define launch arguments
    example_file_arg = DeclareLaunchArgument(
        'example_file',
        default_value='tutorial.py',
        description='Python API tutorial file name'
    )

    # Define nodes
    moveit_py_node = Node(
        package='moveit_python_api',
        executable='tutorial',
        name='tutorial',
        output='both',
        arguments=[LaunchConfiguration('example_file')]
    )

    rviz_config_file = os.path.join(
        get_package_share_directory('moveit_python_api'),
        'config',
        'motion_plan.rviz'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='log',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        example_file_arg,
        moveit_py_node,
        rviz_node
    ])