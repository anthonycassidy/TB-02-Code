#!/usr/bin/env python3
import os
import sys
import logging
import subprocess
import time
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeploymentWizard:
    def __init__(self):
        self.checks_passed = 0
        self.total_checks = 6
        self.is_raspberry_pi = False
    
    def print_progress(self, message: str) -> None:
        """Print a formatted progress message"""
        logger.info(f"[{self.checks_passed}/{self.total_checks}] {message}")
    
    def check_platform(self) -> bool:
        """Verify if running on Raspberry Pi"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            self.is_raspberry_pi = 'Raspberry Pi 5' in cpuinfo
            if not self.is_raspberry_pi:
                logger.error("This script must be run on a Raspberry Pi 5")
                return False
            self.checks_passed += 1
            self.print_progress("Platform check passed")
            return True
        except Exception as e:
            logger.error(f"Failed to verify platform: {e}")
            return False

    def check_dependencies(self) -> bool:
        """Check required system dependencies"""
        required_packages = [
            'python3-pip',
            'python3-picamera2',
            'python3-libcamera',
            'i2c-tools',
            'python3-smbus'
        ]
        
        try:
            for package in required_packages:
                result = subprocess.run(['dpkg', '-s', package], 
                                     capture_output=True, text=True)
                if result.returncode != 0:
                    logger.error(f"Missing required package: {package}")
                    return False
            
            self.checks_passed += 1
            self.print_progress("Dependency check passed")
            return True
        except Exception as e:
            logger.error(f"Failed to check dependencies: {e}")
            return False

    def check_interfaces(self) -> bool:
        """Verify if required interfaces are enabled"""
        try:
            # Check I2C
            i2c_result = subprocess.run(['i2cdetect', '-y', '1'], 
                                      capture_output=True, text=True)
            if "Error" in i2c_result.stderr:
                logger.error("I2C interface is not enabled")
                return False
                
            # Check Camera
            if not os.path.exists('/dev/video0'):
                logger.error("Camera interface is not enabled")
                return False
                
            self.checks_passed += 1
            self.print_progress("Interface check passed")
            return True
        except Exception as e:
            logger.error(f"Failed to check interfaces: {e}")
            return False

    def check_gpio_connections(self) -> bool:
        """Test GPIO connections for motors and servos"""
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            
            # Test motor controller pins
            motor_pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13]
            for pin in motor_pins:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
            
            # Test servo pins
            servo_pins = [14, 15, 18, 23]
            for pin in servo_pins:
                GPIO.setup(pin, GPIO.OUT)
                pwm = GPIO.PWM(pin, 50)
                pwm.start(7.5)
                time.sleep(0.1)
                pwm.stop()
            
            GPIO.cleanup()
            self.checks_passed += 1
            self.print_progress("GPIO connection check passed")
            return True
        except Exception as e:
            logger.error(f"Failed to check GPIO connections: {e}")
            return False

    def setup_service(self) -> bool:
        """Configure systemd service for auto-start"""
        service_content = """[Unit]
Description=Robot Control Interface
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/robot-control/app.py
WorkingDirectory=/opt/robot-control
User=pi
Group=pi
Restart=always

[Install]
WantedBy=multi-user.target
"""
        try:
            if not os.path.exists('/opt/robot-control'):
                os.makedirs('/opt/robot-control')
            
            # Copy application files
            subprocess.run(['cp', '-r', '.', '/opt/robot-control/'])
            
            # Create service file
            with open('/etc/systemd/system/robot-control.service', 'w') as f:
                f.write(service_content)
            
            # Enable and start service
            subprocess.run(['systemctl', 'enable', 'robot-control'])
            subprocess.run(['systemctl', 'start', 'robot-control'])
            
            self.checks_passed += 1
            self.print_progress("Service setup completed")
            return True
        except Exception as e:
            logger.error(f"Failed to setup service: {e}")
            return False

    def verify_application(self) -> bool:
        """Verify if the application is running"""
        try:
            # Wait for service to start
            time.sleep(5)
            result = subprocess.run(['systemctl', 'is-active', 'robot-control'],
                                  capture_output=True, text=True)
            if result.stdout.strip() != 'active':
                logger.error("Service failed to start")
                return False
            
            self.checks_passed += 1
            self.print_progress("Application verification passed")
            return True
        except Exception as e:
            logger.error(f"Failed to verify application: {e}")
            return False

    def run_deployment(self) -> bool:
        """Run all deployment checks and setup"""
        logger.info("Starting Robot Control Interface deployment...")
        
        checks = [
            self.check_platform,
            self.check_dependencies,
            self.check_interfaces,
            self.check_gpio_connections,
            self.setup_service,
            self.verify_application
        ]
        
        for check in checks:
            if not check():
                logger.error("Deployment failed!")
                return False
        
        logger.info("Deployment completed successfully!")
        logger.info("The robot control interface is now accessible at:")
        logger.info("http://<raspberry-pi-ip>:5000")
        return True

if __name__ == "__main__":
    wizard = DeploymentWizard()
    sys.exit(0 if wizard.run_deployment() else 1)
