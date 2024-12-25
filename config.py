# GPIO Pin Configuration
MOTOR_PINS = {
    'FRONT_LEFT': {
        'EN': 2,
        'IN1': 3,
        'IN2': 4
    },
    'FRONT_RIGHT': {
        'EN': 17,
        'IN1': 27,
        'IN2': 22
    },
    'REAR_LEFT': {
        'EN': 10,
        'IN1': 9,
        'IN2': 11
    },
    'REAR_RIGHT': {
        'EN': 5,
        'IN1': 6,
        'IN2': 13
    }
}

SERVO_PINS = {
    'FRONT_LEFT': 14,
    'FRONT_RIGHT': 15,
    'REAR_LEFT': 18,
    'REAR_RIGHT': 23
}

# Battery Monitoring Configuration
BATTERY_ADC_PIN = 26  # GPIO26 for battery voltage monitoring
BATTERY_CHECK_INTERVAL = 10  # seconds
BATTERY_ALERT_THRESHOLD = 10.8  # volts for 3S LiPo (3.6V per cell)
BATTERY_CRITICAL_THRESHOLD = 10.2  # volts
BATTERY_MAX_VOLTAGE = 12.6  # volts (fully charged 3S LiPo)

# Camera Configuration
CAMERA_RESOLUTION = (640, 480)
CAMERA_FRAMERATE = 24
CAMERA_ROTATION = 180  # Adjust based on camera mounting

# Web Interface Configuration
WEB_PORT = 5000
SOCKET_PORT = 8000