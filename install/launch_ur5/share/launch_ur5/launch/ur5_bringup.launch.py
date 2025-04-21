from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command  # 导入 Command
import os

def generate_launch_description():
    ur_package = get_package_share_directory('ur_description')
    
    return LaunchDescription([
        # 加载 UR5 模型（通过 xacro 文件）
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': 
                    Command(['xacro ', os.path.join(ur_package, 'urdf/ur_macro.xacro')])
            }]
        ),
        # 启动 Joint State Publisher（用于手动调节关节）
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        # 启动 RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', os.path.join(ur_package, 'config/ur5.rviz')]
        )
    ])