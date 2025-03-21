import cv2
import depthai as dai
import numpy as np
import serial
import time
from numpy import interp

import rclpy
from rclpy.node import Node

from ucsd_robocar_nav2_pkg.car_control import moveCar
from ucsd_robocar_nav2_pkg.PID import controlPID

from gps_april_msgs.msg import GpsApril


class AprilTag(Node):
	def __init__(self):
		super().__init__("april_tag_node"); 
		self.declare_parameter('detect', False); 
		self.declare_parameter('visualize', False); 
		
		self.checkDetect = self.get_parameter('detect').value; 
		self.checkVisualize = self.get_parameter('detect').value; 
		
		self.talkPublisher = self.create_publisher(GpsApril, '/talkGpsApril', 10); 
		self.talkSubscriber = self.create_subscription(
			GpsApril,
			'/talkGpsApril',
			self.GpsAprilChecker,
			10
		); 
		self.talkSubscriber; 
		
		self.theCar = moveCar(); 
		self.theCar.stopCar(); 
		self.PID = controlPID(Kp = 0.4, Ki = 0, Kd = 0.15, theError = 0.0); 
		
		self.targetID = 0; 
		self.theThreshold = 12000; # Box is about 6in away
		
		self.theSerial = serial.Serial(port = "/dev/ttyACM0", baudrate = 9600); 
		
		self.aprilMode = False; 
	
		if self.checkDetect: 
			self.aprilDetection(); 
			
	def GpsAprilChecker(self, theMessage):
		self.get_logger().info("Message Received: " + str(theMessage)); 
		self.aprilMode = theMessage.april_mode; 
	
	
	def aprilDetection(self): 
		thePipeline = dai.Pipeline(); 
		cameraRGB = thePipeline.create(dai.node.ColorCamera); 
		# print(str(cameraRGB.getResolution())); 
		cameraRGB.setPreviewSize(960, 540); # Our camera is 1080, so 1920 x 1080 frame size
		cameraRGB.setInterleaved(False); 
		cameraRGB.setFps(30); 
		
		aprilTag = thePipeline.create(dai.node.AprilTag); 
		cameraRGB.video.link(aprilTag.inputImage); 
		
		xOutDetections = thePipeline.create(dai.node.XLinkOut); 
		xOutDetections.setStreamName("Detection Stream"); 
		aprilTag.out.link(xOutDetections.input); 
		
		xOutVideo = thePipeline.create(dai.node.XLinkOut); 
		xOutVideo.setStreamName("Video Stream"); 
		cameraRGB.preview.link(xOutVideo.input); 
			
		with dai.Device(thePipeline) as theDevice:
			aprilQueue = theDevice.getOutputQueue(name = "Detection Stream", maxSize = 4, blocking = False);
			videoQueue = theDevice.getOutputQueue(name = "Video Stream", maxSize = 4, blocking = False);
		
			while True: 
				if self.aprilMode:
					try:
						theDetections = aprilQueue.get(); 
					except RuntimeError as theError:
						self.get_logger().info("Camera Error: " + str(theError));
						time.sleep(4); 
						continue; 
							
					theFrame = videoQueue.get().getCvFrame(); 
					
					if self.checkVisualize: 
						cv2.line(theFrame, (480, 540), (480, 0), (0, 255, 0), 2); 
				
					if theDetections is not None: 
						for aDetection in theDetections.aprilTags:
							tagID = aDetection.id; 
							# self.get_logger().info("Tag ID: " + str(tagID));  
							# Map coordinate to our preview size using interpolate
							xBR = aDetection.bottomRight.x; 
							xBR = int(np.interp(xBR, [0, 1920], [0, 960])); 
							yBR = aDetection.bottomRight.y; 
							yBR = int(np.interp(yBR, [0, 1080], [0, 540])); 
							# self.get_logger().info("Bottom Right Coordinate: " + str(xBR) + ", " + str(yBR)); 
							
							xTL = aDetection.topLeft.x; 
							xTL = int(np.interp(xTL, [0, 1920], [0, 960])); 
							yTL = aDetection.topLeft.y; 
							yTL = int(np.interp(yTL, [0, 1080], [0, 540])); 
							# self.get_logger().info("Top Left Coordinate: " + str(xTL) + ", " + str(yTL)); 
							
							xMiddle = int(xBR - ((xBR - xTL)/2)); 
							yMiddle = int(yTL - ((yTL - yBR)/2)); 
								
							theError = xMiddle - 480; 
							self.get_logger().info("Error: " + str(theError)); 
							
							theHeight = int(yTL - yBR); 
							theWidth = int(xBR - xTL); 
							
							theArea = np.abs(theHeight * theWidth); 
							self.get_logger().info("Area: " + str(theArea)); 
						
							if tagID == self.targetID:
								if theArea < self.theThreshold:
									theAngle = self.PID.computePID(theError); 
									theAngle = np.interp(theAngle, [-180, 180], [-0.5, 0.5]); 
									self.get_logger().info("Angle: " + str(theAngle)); 
									self.theCar.driveCar(0.3, theAngle); 
									time.sleep(1); 
									
								if theArea > self.theThreshold:
									self.theSerial.write("on".encode('Ascii')); 
									time.sleep(1); 
								
									theAngle = self.PID.computePID(theError); 
									theAngle = np.interp(theAngle, [-180, 180], [-0.5, 0.5]); 
									self.get_logger().info("Angle: " + str(theAngle)); 
									self.theCar.driveCar(0.4, theAngle); 
									time.sleep(2); 
									self.theCar.driveCar(-0.3, 0.0); 
									
									self.theCar.turnAround(); 
									self.theCar.driveCar(0.5, 0.0); 
									self.theSerial.write("off".encode('Ascii')); 
									self.theSerial.close(); 
									time.sleep(2); 
									self.theCar.driveCar(-0.5, 0.0); 
								
							if self.checkVisualize:
								cv2.rectangle(theFrame, (xTL, yTL), (xBR, yBR), (255, 0, 0), 2); 
								cv2.line(theFrame, (xMiddle, yMiddle), (480, yMiddle), (0, 0, 255), 2); 
								cv2.putText(theFrame, str(tagID), (xMiddle, yMiddle), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA); 
							 				
					 
					if self.checkVisualize:
						cv2.imshow("April Tag", theFrame); 
					
					if cv2.waitKey(1) and 0xFF == ord('q'):
						break; 
						
				cv2.destroyAllWindows(); 
				 
				 

def main(args = None): 
	rclpy.init(args = args); 
	
	nodeAprilTag = AprilTag(); 
	
	rclpy.spin(nodeAprilTag); 
	
	rclpy.shutdown(); 
	
	
	
if __name__ == '__main__':
	main(); 
