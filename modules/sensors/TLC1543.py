import RPi.GPIO as GPIO

class TLC1543(object):
	
	def __init__(self):
		self.CS = 5
		self.DOUT = 23
		self.ADDR = 24
		self.IOCLK = 25
		
	#def setup(self):