import RPi.GPIO as GPIO

class IR(object):
	
	def __init__(self):
		self.IR = 17
		
	def setup(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.IR, GPIO.IN)