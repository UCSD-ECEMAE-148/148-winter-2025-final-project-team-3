import time


class controlPID():  
	def __init__(self, Kp, Ki, Kd, theError = 0): 
		self.previousError = theError; 
		self.previousTime = time.time(); 
		self.integralTerm = 0;  
		
		self.Kp = Kp; 
		self.Ki = Ki; 
		self.Kd = Kd; 
		
		
	def computePID(self, theError): 
		currentTime = time.time(); 
		errorDifference = theError - self.previousError; 
		timeDifference = currentTime - self.previousTime; 
		
		if timeDifference == 0: 
			timeDifference = 1; # Prevent division by 0 
		
		proportionalTerm = self.Kp * theError; 
		
		self.integralTerm += theError * timeDifference; 
		integralTerm = self.Ki *self.integralTerm; 
		
		derivativeTerm = errorDifference / timeDifference; 
		derivativeTerm = self.Kd * derivativeTerm; 
		
		PID = proportionalTerm + integralTerm + derivativeTerm; 
		
		self.previousError = theError; 
		self.previousTime = currentTime; 
		
		return PID; 
