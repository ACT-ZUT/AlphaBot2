import RPi.GPIO as GPIO
import time
from modules.AlphaBot2 import AlphaBot2
from inputs import get_gamepad

if __name__=='__main__':
    #max value
	#255    xbox 360 pad (8 bit)
    #1024   xbox one s pad (10 bit)
    scaler = 255 
	robot = AlphaBot2()
	try:
		GPIO.output(robot.TB6612FNG.AIN1,GPIO.LOW)
		GPIO.output(robot.TB6612FNG.AIN2,GPIO.HIGH)
		GPIO.output(robot.TB6612FNG.BIN1,GPIO.LOW)
		GPIO.output(robot.TB6612FNG.BIN2,GPIO.HIGH)
		while True:
			events = get_gamepad()
			for event in events:
				if (event.code == "ABS_RZ"): #right trigger
					power = round(event.state / scaler * 100)
					print("left", event.state, power)
                    #left wheel forward / turn right
					robot.TB6612FNG.setPWMA(power) 

				elif (event.code == "ABS_Z"): #left trigger
					power = round(event.state / scaler * 100)
					print("right", event.state, power)
                    #right wheel forward / turn left
					robot.TB6612FNG.setPWMB(power)
	except KeyboardInterrupt:
		GPIO.cleanup()