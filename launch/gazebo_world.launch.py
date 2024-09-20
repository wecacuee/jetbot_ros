import os

from launch import LaunchDescription
from launch.actions import (IncludeLaunchDescription, DeclareLaunchArgument,
                            AppendEnvironmentVariable)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (ThisLaunchFileDir,
                                  LaunchConfiguration,
                                  PathJoinSubstitution)
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description(pkg_name='jetbot_ros'):
    pkg_dir = FindPackageShare(pkg_name)
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')

    robot_name = DeclareLaunchArgument('robot_name', default_value='jetbot')
    robot_model = DeclareLaunchArgument('robot_model',
                                        default_value='simple_diff_ros')  # jetbot_ros
    robot_x = DeclareLaunchArgument('x', default_value='-0.3')
    robot_y = DeclareLaunchArgument('y', default_value='-2.65')
    robot_z = DeclareLaunchArgument('z', default_value='0.0')

    urdf_path = PathJoinSubstitution([
            pkg_dir,
            'models',
            LaunchConfiguration('robot_model'),
            'model.sdf'
            ])

    world = PathJoinSubstitution([pkg_dir, 'worlds',  'dirt_path_curves.world'])
    launch_file_dir = PathJoinSubstitution([pkg_dir, 'launch'])

    set_env_vars_resources = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        PathJoinSubstitution([pkg_dir, 'gazebo', 'models']))

    ros_gz_sim = FindPackageShare('ros_gz_sim')
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([ros_gz_sim, 'launch', 'gz_sim.launch.py'])
        ),
        launch_arguments={'gz_args': ['-r -s -v4 ', world],
                          'on_exit_shutdown': 'true'}.items()
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([ros_gz_sim, 'launch', 'gz_sim.launch.py'])
        ),
        launch_arguments={'gz_args': '-g -v4 '}.items()
    )


    spawn_entity = Node(package='ros_gz_sim',
                        executable='create',
                        arguments=[
                            '-name', LaunchConfiguration('robot_name'),
                            '-file', urdf_path ,
                            '-x', LaunchConfiguration('x'),
                            '-y', LaunchConfiguration('y'),
                            '-z', LaunchConfiguration('z'),
                        ],
                        output='screen', emulate_tty=True)

    bridge_params = PathJoinSubstitution([
            pkg_dir,
            'params',
            'jetbot_ros_gz_bridge.yaml'
            ])
    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_params}],
        output='screen'
    )

    start_gazebo_ros_image_bridge_cmd = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['/camera/image_raw'],
        output='screen',
    )

    return LaunchDescription([
        set_env_vars_resources,
        robot_name,
        robot_model,
        robot_x,
        robot_y,
        robot_z,
        gzserver_cmd,
        gzclient_cmd,
        spawn_entity,
        start_gazebo_ros_bridge_cmd,
        start_gazebo_ros_image_bridge_cmd
    ])
