import RPi.GPIO as GPIO

class Joystick(object):
	
	def __init__(self):
		self.BUTTON = 7
		self.A = 8
		self.B = 9
		self.C = 10
		self.D = 11
		
	def setup(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.BUTTON, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.A, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.B, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.C, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.D, GPIO.IN, GPIO.PUD_UP)