import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    package_name = 'my_robot'

    # 1. Read and process the XACRO file
    xacro_file = os.path.join(get_package_share_directory(package_name), 'urdf', 'robot.urdf.xacro')
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # 2. Robot State Publisher Node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw, 'use_sim_time': True}]
    )

    # 3. Gazebo Simulator Launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # 4. Spawn Robot Entity in Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'racecar'],
        output='screen'
    )
    #5.ros-gazebo bridge
    bridge=Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'
        ],
        remappings=[
            ('/world/empty/model/racecar/joint_state','joint_states')
        ],
        output='screen'
    )
    

    # 6. RViz2 Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen'
    )
    #7.joint state publisher
    node_joint_state_publisher = Node(
            package='robot_joint_publisher',
            executable='joint_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': True}]
        )
    

    return LaunchDescription([
        node_robot_state_publisher,
        node_joint_state_publisher,
        gazebo,
        spawn_entity,
        bridge,
        rviz_node
    ])