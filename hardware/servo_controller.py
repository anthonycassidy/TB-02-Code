try:
    import RPi.GPIO as GPIO
except ImportError:
    import hardware.mock_gpio as GPIO
from config import SERVO_PINS
import logging

class ServoController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.setup_pins()
        self.current_angle = {pin: 90 for pin in SERVO_PINS.values()}
        logging.debug("Servo controller initialized")

    def setup_pins(self):
        for pin in SERVO_PINS.values():
            GPIO.setup(pin, GPIO.OUT)
            # Initialize PWM at 50Hz
            pwm = GPIO.PWM(pin, 50)
            pwm.start(7.5)  # Center position (90 degrees)

    def set_angle(self, servo, angle):
        """
        Set servo angle
        :param servo: Servo name (FRONT_LEFT, FRONT_RIGHT, etc.)
        :param angle: 0-180 degrees
        """
        if servo not in SERVO_PINS:
            logging.error(f"Invalid servo name: {servo}")
            return

        # Constrain angle
        angle = max(0, min(180, angle))

        # Convert angle to duty cycle (0° = 2.5%, 180° = 12.5%)
        duty = 2.5 + (angle / 180.0) * 10.0

        pin = SERVO_PINS[servo]
        pwm = GPIO.PWM(pin, 50)
        pwm.start(duty)
        self.current_angle[pin] = angle
        logging.debug(f"Set {servo} to {angle} degrees")

    def center_all(self):
        """Center all servos to 90 degrees"""
        for servo in SERVO_PINS.keys():
            self.set_angle(servo, 90)

    def cleanup(self):
        """Cleanup GPIO pins"""
        self.center_all()
        GPIO.cleanup()