import RPi.GPIO as GPIO

class TB6612FNG():
	
    def __init__(self, scaler_left, scaler_right):
        self.PWMA_PIN = 6
        self.PWMB_PIN = 26
        self.AIN1 = 12
        self.AIN2 = 13
        self.BIN1 = 20
        self.BIN2 = 21
        self.scaler_left = scaler_left
        self.scaler_right = scaler_right

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.PWMA_PIN, GPIO.OUT)
        GPIO.setup(self.PWMB_PIN, GPIO.OUT)
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)

        self.PWMA = GPIO.PWM(self.PWMA_PIN, 500) # channel, frequency
        self.PWMB = GPIO.PWM(self.PWMB_PIN, 500)
        self.PWMA.start(50) # 0-100
        self.PWMB.start(50)
        self.stop()

    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.AIN1,GPIO.LOW)
        GPIO.output(self.AIN2,GPIO.LOW)
        GPIO.output(self.BIN1,GPIO.LOW)
        GPIO.output(self.BIN2,GPIO.LOW)

    def setPWMA(self,value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def setPWMB(self,value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)	

    def speed(self, left, right):
        #left forward
        left = left * self.scaler_left
        right = right * self.scaler_right
        if((left >= 0) and (left <= 100)):
            GPIO.output(self.AIN1,GPIO.LOW)
            GPIO.output(self.AIN2,GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(left)
        #left backward
        elif((left < 0) and (left >= -100)):
            GPIO.output(self.AIN1,GPIO.HIGH)
            GPIO.output(self.AIN2,GPIO.LOW)
            self.PWMA.ChangeDutyCycle(0 - left)
        #right forward
        if((right >= 0) and (right <= 100)):
            GPIO.output(self.BIN1,GPIO.LOW)
            GPIO.output(self.BIN2,GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(right)
        #right backward
        elif((right < 0) and (right >= -100)):
            GPIO.output(self.BIN1,GPIO.HIGH)
            GPIO.output(self.BIN2,GPIO.LOW)
            self.PWMB.ChangeDutyCycle(0 - right)