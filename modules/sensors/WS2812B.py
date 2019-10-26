import RPi.GPIO as GPIO

class WS2812B(object):
	
	def __init__(self):
		self.DIN = 18
		
	#def setup(self):