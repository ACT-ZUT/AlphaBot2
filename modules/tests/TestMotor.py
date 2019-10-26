import unittest, os, time
import RPi.GPIO as GPIO
from .. import AlphaBot2


class TestMotor(unittest.TestCase):
	def setUp(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

	@unittest.skipUnless(os.uname()[4].startswith("arm"), "requires raspberrypi")
	def test_left_forward(self):
		robot = AlphaBot2.AlphaBot2()
		input("\nPress enter when you are ready to test \n - left wheel go forward for 1s")
		robot.speed(30, 0)
		time.sleep(1)
		robot.stop()
		test_value = input("t/f?\n")
		self.assertEqual(test_value, 't')

	@unittest.skipUnless(os.uname()[4].startswith("arm"), "requires raspberrypi")
	def test_left_backward(self):
		robot = AlphaBot2.AlphaBot2()
		input("\nPress enter when you are ready to test \n - left wheel go backward for 1s")
		robot.speed(-30, 0)
		time.sleep(1)
		robot.stop()
		test_value = input("t/f?\n")
		self.assertEqual(test_value, 't')
		
	@unittest.skipUnless(os.uname()[4].startswith("arm"), "requires raspberrypi")
	def test_right_forward(self):
		robot = AlphaBot2.AlphaBot2()
		input("\nPress enter when you are ready to test \n - right wheel go forward for 1s")
		robot.speed(0, 30)
		time.sleep(1)
		robot.stop()
		test_value = input("t/f?\n")
		self.assertEqual(test_value, 't')

	@unittest.skipUnless(os.uname()[4].startswith("arm"), "requires raspberrypi")
	def test_right_backward(self):
		robot = AlphaBot2.AlphaBot2()
		input("\nPress enter when you are ready to test \n - right wheel go backward for 1s")
		robot.speed(0, -30)
		time.sleep(1)
		robot.stop()
		test_value = input("t/f?\n")
		self.assertEqual(test_value, 't')
		
	@unittest.skipUnless(os.uname()[4].startswith("arm"), "requires raspberrypi")
	def test_forward(self):
		robot = AlphaBot2.AlphaBot2()
		input("\nPress enter when you are ready to test \n - both wheels go forward for 1s")
		robot.speed(100, 100)
		time.sleep(1)
		robot.stop()
		test_value = input("t/f?\n")
		self.assertEqual(test_value, 't')
		
	@unittest.skipUnless(os.uname()[4].startswith("arm"), "requires raspberrypi")
	def test_backward(self):
		robot = AlphaBot2.AlphaBot2()
		input("\nPress enter when you are ready to test \n - both wheels go backward for 1s")
		robot.speed(-30, -30)
		time.sleep(1)
		robot.stop()
		test_value = input("t/f?\n")
		self.assertEqual(test_value, 't')
		
	def tearDown(self):
		GPIO.cleanup()

if __name__ == '__main__':
	unittest.main()