# Hardware Setup Guide

## GPIO Pin Layout

### Motor Controllers (L298N)
- Front Left Motor:
  * Enable: GPIO2
  * Input 1: GPIO3
  * Input 2: GPIO4

- Front Right Motor:
  * Enable: GPIO17
  * Input 1: GPIO27
  * Input 2: GPIO22

- Rear Left Motor:
  * Enable: GPIO10
  * Input 1: GPIO9
  * Input 2: GPIO11

- Rear Right Motor:
  * Enable: GPIO5
  * Input 1: GPIO6
  * Input 2: GPIO13

### Servo Motors
- Front Left: GPIO14
- Front Right: GPIO15
- Rear Left: GPIO18
- Rear Right: GPIO23

## Wiring Instructions

### L298N Motor Driver Setup
1. Connect power supply (6-12V) to L298N power terminals
2. Connect L298N ground to Raspberry Pi ground
3. Connect motor outputs to DC motors
4. Connect control pins as per GPIO layout
5. Enable jumpers must be removed for PWM control

### Servo Setup
1. Connect servo power to 5V supply
2. Connect servo ground to Raspberry Pi ground
3. Connect signal wires to GPIO pins as specified
4. Ensure adequate power supply for servos

### Camera Module
1. Connect ribbon cable to camera port
2. Secure camera module to robot chassis
3. Orient camera as needed (adjust rotation in config)

## Power Supply Considerations
- Use separate power supply for motors
- Use regulated 5V supply for servos
- Ensure common ground between all components
