import RPi.GPIO as GPIO
import time
import sys
from modules.AlphaBot2 import AlphaBot2
from modules.Kalman import Kalman
from modules.PID import PID
from inputs import get_gamepad

if __name__=='__main__':

    #Open file to write logs
    timestr = time.strftime("%Y%m%d-%H%M%S")
    f = open(timestr + ".txt", "w")

    #Check command line arguments
    if len(sys.argv) < 2:
        setpoint = 30 #default to 30 cm
    else:
        setpoint = float(sys.argv[1])

    #Initialize needed classes
    robot = AlphaBot2(scaler_left = 0.96)
    myFilter = Kalman(1.5, 16, 1023, 0)
    pid = PID(5, 0, 0, setpoint)

    #Set complementary variables
    sample_time = 0.06
    start_time = time.time()
    prev_time = start_time

    try:
        while True:
            if not GPIO.input(robot.LM293.DSL) or not GPIO.input(robot.LM293.DSR):
                robot.stop()
                continue
            #Start/reset timer
            curr_time = time.time()

            #Write difference between last run loop
            delta_time = curr_time - prev_time

            #Run loop every defined sample time or more
            if delta_time >= sample_time:
                #Get raw distance measurement
                raw_dist = robot.dist()
                #Filter distance measurement
                distance = myFilter(raw_dist)
                #Log - (time from start, distance)
                f.write(f"{curr_time - start_time}, {distance}\n")

                curr_pid, I, last_error = pid.calculate(delta_time, I, last_error)
                #Check if values aren't over 100
                #Possible to map them differently
                if curr_pid > 100:
                    curr_pid = 100
                elif curr_pid < -100:
                    curr_pid = -100

                #Normal values
                if curr_pid < -15:
                    robot.backward(abs(curr_pid))
                elif curr_pid > 15:
                    robot.forward(curr_pid)
                
                #Hysteresis
                elif 3 < curr_pid <= 15:
                    robot.forward(15)
                elif -15 < curr_pid < -3:
                    robot.backward(15)
                
                #Stop the robot if value = -3 <-> 3
                else:
                    robot.stop()

                prev_time = curr_time

	            #DEBUGGING
                print(f"DISTANCE: {distance:5.3f}, PID VALUE: {curr_pid:5.3f}")

            
    except KeyboardInterrupt:
        GPIO.cleanup() #Cleanup RPi pins
        f.close() #Close log file

