import RPi.GPIO as GPIO
#import smbus2 as smbus

class PCA9685(object):
	
	def __init__(self):
		self.SDA = 2
		self.SCL = 3

	def setup(self, address = 0x40, debug = True):
		self.bus = smbus.SMBus(1)
		self.address = address
		self.debug = debug
		if (self.debug):
			print("Reseting PCA9685")
		self.write(self.__MODE1, 0x00)

	def write(self, register, value):	
		"""Writes an 8-bit value to the specified register/address

        :param register: Register to write to
        :type register: int
        :param value: Byte value to transmit
        :type value: int
        """
		self.bus.write_byte_data(self.address, register, value)
		if (self.debug):
			print(f"I2C: Write 0x{value:02X} to register 0x{register:02X}")

	def read(self, register):
		"""Read an unsigned byte from the I2C device

		:param register: Register to write to
        :type register: int
		"""
		result = self.bus.read_byte_data(self.address, register)
		if (self.debug):
			print("I2C: Device 0x{self.address:02X} returned 0x{result&0xFF:02X} from register 0x{register:02X}")
		return result