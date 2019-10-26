import RPi.GPIO as GPIO

class Buzzer(object):
	
	def __init__(self):
		self.BUZZER = 4

	def setup(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.BUZZER, GPIO.OUT)