"""Mock GPIO module for development environment"""
import logging

# GPIO numbering modes
BCM = 11
BOARD = 10

# Pin states
HIGH = 1
LOW = 0

# Pin modes
OUT = 1
IN = 0

_pin_states = {}
_pin_modes = {}

def setmode(mode):
    logging.debug(f"GPIO setmode: {mode}")

def setup(pin, mode):
    _pin_modes[pin] = mode
    _pin_states[pin] = LOW
    logging.debug(f"GPIO setup pin {pin} as {'output' if mode == OUT else 'input'}")

def output(pin, state):
    _pin_states[pin] = state
    logging.debug(f"GPIO output pin {pin}: {state}")

def cleanup():
    _pin_states.clear()
    _pin_modes.clear()
    logging.debug("GPIO cleanup")

class PWM:
    def __init__(self, pin, frequency):
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = 0
        logging.debug(f"PWM initialized on pin {pin} at {frequency}Hz")

    def start(self, duty_cycle):
        self.duty_cycle = duty_cycle
        logging.debug(f"PWM started on pin {self.pin} with duty cycle {duty_cycle}")

    def ChangeDutyCycle(self, duty_cycle):
        self.duty_cycle = duty_cycle
        logging.debug(f"PWM duty cycle changed to {duty_cycle} on pin {self.pin}")

    def stop(self):
        logging.debug(f"PWM stopped on pin {self.pin}")