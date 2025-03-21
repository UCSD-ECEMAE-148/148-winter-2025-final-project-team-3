import os
import pandas as pd
import numpy as np
import pymap3d as pmap

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

from sensor_msgs.msg import NavSatFix
from ucsd_robocar_nav2_pkg.car_control import moveCar
from ucsd_robocar_nav2_pkg.PID import controlPID

from gps_april_msgs.msg import GpsApril


class gpsNavigationNode(Node):
	def __init__(self):
		super().__init__("gps_navigation_node"); 
		# self.get_logger().info("GPS Node Activated!");

		# self.get_logger().info(str(os.getcwd()));
		dataFrame = pd.read_csv("src/ucsd_robocar_hub2/ucsd_robocar_nav2_pkg/ucsd_robocar_nav2_pkg/coordinates.csv");

		# theData = self.parseData(dataFrame);

		# self.get_logger().info(str(theData['A']));

		theQoS = QoSProfile(depth = 10, reliability=ReliabilityPolicy.BEST_EFFORT, durability=DurabilityPolicy.VOLATILE);
		self.theSubscriber = self.create_subscription(
			NavSatFix,
			'/fix',
			self.getCoordinate,
			theQoS
		); 
		self.theSubscriber; 
		
		self.talkPublisher = self.create_publisher(GpsApril, '/talkGpsApril', 10);
		self.talkSubscriber = self.create_subscription(
			GpsApril,
			'/talkGpsApril',
			self.GpsAprilChecker,
			10
		); 
		self.talkSubscriber; 


		self.theLat0 = 32.88115036131583; 
		self.theLon0 = -117.23339932288448; 
		self.theAlt0 = 74.33511395566165; 

		csvInfo = self.parseData(dataFrame); 
		self.theTarget = csvInfo['A']; 
		self.theTargetE = self.theTarget[0]; 
		self.theTargetN = self.theTarget[1]; 
		
		# Initialize interface, we start with GPS
		theMessage = GpsApril(); 
		theMessage.target_name = "A"; 
		theMessage.approach_target = True; 
		theMessage.gps_mode = True; 
		self.talkPublisher.publish(theMessage); 
		
		self.PID = controlPID(Kp = 0.2, Ki = 0, Kd = 0.12, theError = 0.0); 
		self.theCar = moveCar(); 
		self.theCar.stopCar(); 
		
		self.approachTarget = False; 
		self.returnOrigin = False; 
		self.targetName = ""; 
		self.gpsMode = False; 
		
		
	def GpsAprilChecker(self, theMessage):
		self.get_logger().info("Message Received: " + str(theMessage)); 
		self.approachTarget = theMessage.approach_target; 
		self.returnOrigin = theMessage.return_origin; 
		self.targetName = theMessage.target_name; 
		self.gpsMode = theMessage.gps_mode; 
		
		
	def euclideanDistance(self, theE, theN, theU):
		theDistance = np.sqrt((self.theTargetE - theE)**2 + (self.theTargetN - theN)**2);
		return theDistance; 


	def lineSide(self, theE, theN): # Which side of the line we are on using the determinant of two vectors
		# Determine the side of the line we are on using sign function
		# det = (x2 - x1)*(p_y - y1) - (y2 - y1)*(p_x - x1);
		# Origin = (x1, y1), Target = (x2, y2), Point = (p_x, p_y);
		# We want to check if the point is on the left or right of the line made by origin and target
		# If the determinant is greater than 0 it is left, less than it is right, exactly 0 is on line
		x1 = 0; y1 = 0; x2 = self.theTargetE; y2 = self.theTargetN; 
		p_x = theE; p_y = theN; 
		theDeterminant = (x2 - x1)*(p_y - y1) - (y2 - y1)*(p_x - x1); 
		return np.sign(theDeterminant); 
		
		
	def crossTrackError(self, theE, theN): # How far a point is from a line
		# Distance from line = Ax + By + C / sqrt(A**2 + B**2);
		# Ax + By + C = 0, y = mx + b, mx - y + b = 0, C = b, B = -1, A = m
		A = self.theTargetN/self.theTargetE; B = -1; C = 0; 
		x = theE; y = theN; 
		CTE = (np.abs(A*x + B*y + C) / np.sqrt(A**2 + B**2)); 
		return CTE; 
		
		
	def driveTarget(self, theE, theN, theU):
		# self.get_logger().info(str(self.gpsMode)); 
		if self.gpsMode and self.approachTarget:
			theDistance = self.euclideanDistance(theE, theN, theU); 
			self.get_logger().info("Euclidean Distance: " + str(theDistance)); 

			theCTE = self.crossTrackError(theE, theN); # Distance from line
			theCTE = theCTE*self.lineSide(theE, theN); # Side of line
			self.get_logger().info("Cross Track Error: " + str(theCTE)); 

			if theDistance < 0.7:
				self.theCar.stopCar(); 
				theMessage = GpsApril(); 
				theMessage.approach_target = False; 
				theMessage.gps_mode = False; 
				theMessage.april_mode = True; 
				self.talkPublisher.publish(theMessage); 

			else:
				theAngle = self.PID.computePID(theCTE); 
				self.get_logger().info("Angle: " + str(theAngle)); 
				self.theCar.continuousDrive(0.3, theAngle); 


	def getCoordinate(self, theMessage):
		NS = theMessage.latitude; # (+) = North, (-) = South
		EW = theMessage.longitude; # (+) = East, (-) = West
		ALT = theMessage.altitude; 
		self.get_logger().info(f"East: {EW}, North: {NS},  Alt: {ALT}"); 

		# Convert to ENU
		theE, theN, theU = pmap.geodetic2enu(NS, EW, ALT, self.theLat0, self.theLon0, self.theAlt0); 

		self.get_logger().info(f"E: {theE}, N: {theN}, U: {theU}"); 
		self.driveTarget(theE, theN, theU); 


	def parseData(self, dataFrame):
		dataDictionary = {}; 
		for anIndex, aRow in dataFrame.iterrows():
			# self.get_logger().info(f"Index: {anIndex}");
			# self.get_logger().info(f"Warehouse: {aRow['warehouse']}, East: {aRow['east']}, North: {aRow['north']}");
			dataDictionary.update({aRow['warehouse']: (aRow['east'], aRow['north'], aRow['up'])}); 
		return dataDictionary; 


def main(args = None):
	rclpy.init(args = args); 

	gpsNode = gpsNavigationNode(); 

	rclpy.spin(gpsNode); 

	gpsNode.destroy_node(); 
	rclpy.shutdown(); 


if __name__ == '__main__':
	main(); 
