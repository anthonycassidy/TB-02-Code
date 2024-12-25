try:
    import RPi.GPIO as GPIO
except ImportError:
    import hardware.mock_gpio as GPIO
from config import MOTOR_PINS
import logging

class MotorController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.setup_pins()
        self.current_speed = 0
        logging.debug("Motor controller initialized")

    def setup_pins(self):
        for motor in MOTOR_PINS.values():
            GPIO.setup(motor['EN'], GPIO.OUT)
            GPIO.setup(motor['IN1'], GPIO.OUT)
            GPIO.setup(motor['IN2'], GPIO.OUT)
            # Setup PWM for speed control
            GPIO.output(motor['EN'], GPIO.HIGH)

    def set_motor_direction(self, motor, forward=True):
        pins = MOTOR_PINS[motor]
        if forward:
            GPIO.output(pins['IN1'], GPIO.HIGH)
            GPIO.output(pins['IN2'], GPIO.LOW)
        else:
            GPIO.output(pins['IN1'], GPIO.LOW)
            GPIO.output(pins['IN2'], GPIO.HIGH)

    def set_speed(self, speed):
        """
        Set speed for all motors
        :param speed: -100 to 100 (negative for reverse)
        """
        self.current_speed = speed
        direction = speed >= 0
        abs_speed = abs(speed)

        for motor in MOTOR_PINS.keys():
            self.set_motor_direction(motor, direction)
            # Adjust PWM duty cycle based on speed
            pwm = GPIO.PWM(MOTOR_PINS[motor]['EN'], 1000)
            pwm.start(abs_speed)

    def stop(self):
        """Emergency stop all motors"""
        for motor in MOTOR_PINS.values():
            GPIO.output(motor['IN1'], GPIO.LOW)
            GPIO.output(motor['IN2'], GPIO.LOW)
        self.current_speed = 0
        logging.debug("Emergency stop activated")

    def cleanup(self):
        """Cleanup GPIO pins"""
        self.stop()
        GPIO.cleanup()