class Kalman():

    def __init__(self, process_noise, sensor_noise, estimated_error, initial_value):
        self.q = process_noise
        self.r = sensor_noise
        self.p = estimated_error
        self.x = initial_value
        self.k = 0
    
    def get_filtered_value(self, measurement):
        self.p += self.q
        self.k = self.p / (self.p + self.r)
        self.x += self.k * (measurement - self.x)
        self.p = (1 - self.k) * self.p

        return self.x