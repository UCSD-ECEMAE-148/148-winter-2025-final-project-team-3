import numpy as np
import time
from rclpy.node import Node

from ackermann_msgs.msg import AckermannDriveStamped as ADS


class moveCar(Node): 
    def __init__(self):
    	super().__init__('move_car_node'); 
        self.thePublisher = self.create_publisher(ADS, '/drive', 10); 
        
    
    def driveCar(self, theSpeed, theAngle):
        theMessage = ADS(); 
        theMessage.drive.speed = theSpeed; 
        theMessage.drive.steering_angle = theAngle; 
        self.thePublisher.publish(theMessage); 
        time.sleep(0.5); 
        theMessage.drive.speed = 0.0; 
        self.thePublisher.publish(theMessage); 
        time.sleep(0.5); 
         
    
    def stopCar(self): 
        theMessage = ADS(); 
        theMessage.drive.speed = 0.0; 
        theMessage.drive.steering_angle = 0.0; 
        self.thePublisher.publish(theMessage); 
        time.sleep(0.5)
        
    
    def turnAround(self): 
	    self.driveCar(-0.8, 0.7); 
        self.driveCar(-0.8, 0.7); 
        self.driveCar(-0.8, 0.7); 
        time.sleep(1); 
        self.driveCar(0.8, -0.7); 
        self.driveCar(0.8, -0.7); 
        self.driveCar(0.8, -0.5); time.sleep(1); 
	    
	
    def continuousDrive(self, theSpeed, theAngle):
        theMessage = ADS(); 
        theMessage.drive.speed = theSpeed; 
        theMessage.drive.steering_angle = theAngle; 
        self.thePublisher.publish(theMessage);	    
        
