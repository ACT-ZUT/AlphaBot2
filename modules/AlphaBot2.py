import RPi.GPIO as GPIO
import time
from modules.sensors.Buzzer import Buzzer
from modules.sensors.IR import IR
from modules.sensors.Joystick import Joystick
from modules.sensors.LM293 import LM293
from modules.sensors.PCA9685 import PCA9685
from modules.sensors.SR04 import SR04
from modules.sensors.TB6612FNG import TB6612FNG
from modules.sensors.TLC1543 import TLC1543
from modules.sensors.WS2812B import WS2812B

class AlphaBot2(object):
	
	def __init__(self):
		self.Buzzer = Buzzer()
		self.IR = IR()
		self.Joystick = Joystick()
		self.LM293 = LM293()
		self.PCA9685 = PCA9685()
		self.SR04 = SR04()
		self.TB6612FNG = TB6612FNG()

	def stop(self):
		self.TB6612FNG.stop()
		
	def speed(self, left, right):
		self.TB6612FNG.speed(left, right)