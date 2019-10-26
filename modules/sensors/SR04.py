import RPi.GPIO as GPIO
import asyncio
import time

class SR04(object):
	
	def __init__(self):
		self.TRIG = 22
		self.ECHO = 27
		
	def setup(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.TRIG, GPIO.OUT, initial = GPIO.LOW)
		GPIO.setup(self.ECHO, GPIO.IN)
	
	async def dist():
		GPIO.output(self.TRIG, GPIO.HIGH)
		asyncio.sleep(0.000015)
		GPIO.output(TRIG, GPIO.LOW)
		while not GPIO.input(ECHO):
			pass
		t1 = asyncio.time()
		while GPIO.input(ECHO):
			pass
		t2 = asyncio.time()
		return (t2 - t1) * 34000 / 2
