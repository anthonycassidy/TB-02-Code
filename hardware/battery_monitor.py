try:
    import RPi.GPIO as GPIO
    import busio
    import adafruit_ads1x15.ads1015 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
except ImportError:
    import hardware.mock_gpio as GPIO
    # Mock ADS1015 for development
    class AnalogIn:
        def __init__(self, ads, pin):
            self.voltage = 12.0  # Mock voltage for development
    
    class ADS:
        def __init__(self):
            pass
        
        def get_voltage(self):
            return 12.0

import threading
import time
import logging
from config import (
    BATTERY_ADC_PIN,
    BATTERY_CHECK_INTERVAL,
    BATTERY_ALERT_THRESHOLD,
    BATTERY_CRITICAL_THRESHOLD,
    BATTERY_MAX_VOLTAGE
)

class BatteryMonitor:
    def __init__(self, callback=None):
        """
        Initialize battery monitor
        :param callback: Function to call when battery status changes
        """
        self.callback = callback
        self.current_voltage = 0
        self.percentage = 100
        self.is_low = False
        self.is_critical = False
        self.stopped = False
        
        try:
            # Initialize ADC for battery monitoring
            i2c = busio.I2C(3, 2)  # SCL, SDA
            ads = ADS.ADS1015(i2c)
            self.adc = AnalogIn(ads, BATTERY_ADC_PIN)
        except Exception as e:
            logging.warning(f"Using mock battery monitor: {e}")
            self.adc = AnalogIn(None, BATTERY_ADC_PIN)
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logging.debug("Battery monitor initialized")

    def _monitor_loop(self):
        """Continuous monitoring loop"""
        while not self.stopped:
            self._check_battery()
            time.sleep(BATTERY_CHECK_INTERVAL)

    def _check_battery(self):
        """Check battery voltage and update status"""
        try:
            # Read voltage from ADC
            self.current_voltage = self.adc.voltage
            
            # Calculate battery percentage
            voltage_range = BATTERY_MAX_VOLTAGE - BATTERY_CRITICAL_THRESHOLD
            self.percentage = max(0, min(100, (
                (self.current_voltage - BATTERY_CRITICAL_THRESHOLD) 
                / voltage_range * 100
            )))
            
            # Check alert thresholds
            was_low = self.is_low
            was_critical = self.is_critical
            
            self.is_low = self.current_voltage <= BATTERY_ALERT_THRESHOLD
            self.is_critical = self.current_voltage <= BATTERY_CRITICAL_THRESHOLD
            
            # Notify if status changed
            if self.callback and (was_low != self.is_low or was_critical != self.is_critical):
                self.callback(self.get_status())
                
        except Exception as e:
            logging.error(f"Error reading battery voltage: {e}")

    def get_status(self):
        """Get current battery status"""
        return {
            'voltage': round(self.current_voltage, 1),
            'percentage': round(self.percentage),
            'is_low': self.is_low,
            'is_critical': self.is_critical
        }

    def stop(self):
        """Stop the monitoring thread"""
        self.stopped = True
        if self.monitor_thread.is_alive():
            self.monitor_thread.join()
        logging.debug("Battery monitor stopped")
