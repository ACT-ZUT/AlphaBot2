

class PID():
    def __init__(self, kP, kI, kD, setpoint):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.setpoint = setpoint
        self.error = 0
        self.last_err = 0

    def calculate(delta_time, I, last_error):
        self.error = distance - setpoint
        P = self.error * self.kP
        I += delta_time * self.error * self.kI
        D = ((self.error - last_error) / delta_time) * self.kD
        self.last_err = self.error

        return (P + I + D, I, error)