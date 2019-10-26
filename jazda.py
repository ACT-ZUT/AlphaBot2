import RPi.GPIO as GPIO
import time
from kalman import Kalman
import sys


def forward(speed):
	GPIO.output(AIN1, GPIO.LOW)			#lewo
	GPIO.output(AIN2, GPIO.HIGH)    
	GPIO.output(BIN1, GPIO.LOW)			#prawo
	GPIO.output(BIN2, GPIO.HIGH)
	PWMA.ChangeDutyCycle(speed*0.96)      
	PWMB.ChangeDutyCycle(speed)
		

def stop():
	GPIO.output(AIN1, GPIO.LOW)
	GPIO.output(AIN2, GPIO.LOW)
	GPIO.output(BIN1, GPIO.LOW)
	GPIO.output(BIN2, GPIO.LOW)
	PWMA.ChangeDutyCycle(0)
	PWMB.ChangeDutyCycle(0)
	time.sleep(0.05)


def backward(speed):
	GPIO.output(AIN1, GPIO.HIGH)
	GPIO.output(AIN2, GPIO.LOW)
	GPIO.output(BIN1, GPIO.HIGH)
	GPIO.output(BIN2, GPIO.LOW)
	PWMA.ChangeDutyCycle(speed*0.96)
	PWMB.ChangeDutyCycle(speed)


def turn_in_place_left(speed):
	GPIO.output(AIN1, GPIO.LOW)
	GPIO.output(AIN2, GPIO.LOW)    
	GPIO.output(BIN1, GPIO.LOW)
	GPIO.output(BIN2, GPIO.HIGH)
	PWMA.ChangeDutyCycle(speed)      
	PWMB.ChangeDutyCycle(speed)


def turn_in_place_right(speed):
	GPIO.output(AIN1, GPIO.LOW)
	GPIO.output(AIN2, GPIO.HIGH)    
	GPIO.output(BIN1, GPIO.LOW)
	GPIO.output(BIN2, GPIO.LOW)
	PWMA.ChangeDutyCycle(speed)      
	PWMB.ChangeDutyCycle(speed)


def backward_turn_in_place_right(speed):
	GPIO.output(AIN1, GPIO.HIGH)
	GPIO.output(AIN2, GPIO.LOW)
	GPIO.output(BIN1, GPIO.LOW)
	GPIO.output(BIN2, GPIO.LOW)
	PWMA.ChangeDutyCycle(speed)
	PWMB.ChangeDutyCycle(speed)


def backward_turn_in_place_left(speed):
	GPIO.output(AIN1, GPIO.LOW)
	GPIO.output(AIN2, GPIO.LOW)
	GPIO.output(BIN1, GPIO.HIGH)
	GPIO.output(BIN2, GPIO.LOW)
	PWMA.ChangeDutyCycle(speed)
	PWMB.ChangeDutyCycle(speed)

def get_dist(filter):
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		while GPIO.input(ECHO) == 0:
			start_time = time.time()
		
		while GPIO.input(ECHO) == 1:
			end_time = time.time() 

		dist = (end_time - start_time) * 34300/2 # cm
		dist = filter.get_filtered_value(dist)

		return dist

def calculate_PID(delta_time, I, last_error):
		error = distance - setpoint
		P = error * kP
		I += delta_time * error * kI
		D = ((error - last_error) / delta_time) * kD

		return (P + I + D, I, error)


if __name__=='__main__':

	#robot = AlphaBot2()
	try:
		GPIO.setmode(GPIO.BCM)     #adresy pinow wyjscia
		GPIO.setwarnings(False)
		AIN1 = 12
		AIN2 = 13
		PWMA_pin = 6		# pin na ktorym mozemy ustawic pwm
		BIN1 = 20
		BIN2 = 21
		PWMB_pin = 26
		ECHO = 27
		TRIG = 22		  #funkcja = numer wyjscia na raspberry z obrazka z prezentacji
		DSL = 16
		DSR = 19
		GPIO.setup(AIN1, GPIO.OUT)		     #AIN1 - silnik A w jedna strone
		GPIO.setup(AIN2, GPIO.OUT)		     #AIN1 - silnik A w druga strone
		GPIO.setup(BIN1, GPIO.OUT)
		GPIO.setup(BIN2, GPIO.OUT)
		GPIO.setup(PWMA_pin, GPIO.OUT)		     #PWMA - sygnal PWM do sterowania predkoscia silnika A
		GPIO.setup(PWMB_pin, GPIO.OUT)
		GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)		      #do czujnika odleglosci
		GPIO.setup(ECHO, GPIO.IN)		 #do czujnika odleglosci    
		GPIO.setup(DSL, GPIO.IN)
		GPIO.setup(DSR, GPIO.IN)
		PWMA = GPIO.PWM(PWMA_pin,500)    #PWM tu bedzie z czestotliwoscia 500Hz
		PWMB = GPIO.PWM(PWMB_pin,500)
		PWMA.start(50)
		PWMB.start(50)      #startujemy PWM-a z wypelnieniem 50%
		GPIO.output(AIN1,GPIO.LOW)
		GPIO.output(AIN2,GPIO.LOW)
		GPIO.output(BIN1,GPIO.LOW)
		GPIO.output(BIN2,GPIO.LOW)
		PWMA.ChangeDutyCycle(0)
		PWMB.ChangeDutyCycle(0)	
		
		##########################

		kP = 5
		kI = 0
		kD = 0

		if len(sys.argv) < 2:
			setpoint = 30  # cm
		else:
			setpoint = float(sys.argv[1])
		error = 0
		last_error = 0

		##########################

		myFilter = Kalman(1.5, 16, 1023, 0)

		I = 0
		last_error = 0
		prev_time = time.time()
		sample_time = 0.06

		f = open('data.txt', 'w')
		start_time = time.time()
		while True:
			if not GPIO.input(DSL) or not GPIO.input(DSR):
				stop()
				continue
			curr_time = time.time()
			delta_time = curr_time - prev_time

			# every 10ms (or more)
			if delta_time >= sample_time:
				distance = get_dist(myFilter)
				f.write(f"{curr_time - start_time} {distance}\n")

				curr_pid, I, last_error = calculate_PID(delta_time, I, last_error)
				if curr_pid > 100:
					curr_pid = 100

				if curr_pid < -100:
					curr_pid = -100
				
				if curr_pid < -15:
					backward(abs(curr_pid))
				elif curr_pid > 15:
					forward(curr_pid)

				elif 3 < curr_pid <= 15:
					forward(15)
				elif -15 < curr_pid < -3:
					backward(15)
				
				else:
					stop()

				prev_time = curr_time # or time.time() ?

				# DEBUGGING
				print("DISTANCE: %5.3f, PID VALUE: %5.3f"%(distance,curr_pid))
				# print(distance)
				#print("PID VALUE: ", curr_pid) 
				# print(curr_pid)

	except KeyboardInterrupt:
		GPIO.cleanup()
		f.close()