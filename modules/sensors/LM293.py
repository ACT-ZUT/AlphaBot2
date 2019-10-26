import RPi.GPIO as GPIO

class LM293(object):
	
	def __init__(self):
		self.DSR = 19
		self.DSL = 16

	#def setup(self):