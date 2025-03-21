from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
	detectArg = DeclareLaunchArgument('detect', default_value = "False"); 
	visualizeArg = DeclareLaunchArgument('visualize', default_value = "False"); 


	allNodesLaunch = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			os.path.join(get_package_share_directory('ucsd_robocar_nav2_pkg'), 'launch', 'all_nodes.launch.py')
		)
	); 
	
	aprilTagNode = Node(
		package = 'ucsd_robocar_nav2_pkg',
		executable = 'april_tag_detector_executable',
		output = 'screen',
		parameters = [{
			'detect': LaunchConfiguration('detect'),
			'visualize': LaunchConfiguration('visualize')
		}]
	); 
	
	gpsNavNode = Node(
		package = 'ucsd_robocar_nav2_pkg',
		executable = 'gps_navigation_executable',
		output = 'screen'
	); 


	return LaunchDescription([
		detectArg,
		visualizeArg,
		allNodesLaunch,
		aprilTagNode,
		gpsNavNode
	]); 
