class RobotController {
    constructor() {
        this.socket = io();
        this.connected = false;
        this.setupWebSocket();
        this.setupJoysticks();
        this.setupControls();
    }

    setupWebSocket() {
        this.socket.on('connect', () => {
            this.connected = true;
            this.updateStatus('Connected', 'success');
        });

        this.socket.on('disconnect', () => {
            this.connected = false;
            this.updateStatus('Disconnected', 'danger');
        });

        this.socket.on('error', (error) => {
            console.error('WebSocket error:', error);
            this.updateStatus('Error: ' + error, 'danger');
        });

        // Battery status updates
        this.socket.on('battery_status', (status) => {
            this.updateBatteryStatus(status);
        });

        // Battery alerts
        this.socket.on('battery_alert', (alert) => {
            this.showBatteryAlert(alert);
        });
    }

    setupJoysticks() {
        // Drive joystick (left)
        this.driveJoystick = new VirtualJoystick('drive-joystick', {
            size: 200,
            maxDistance: 75,
            onChange: (pos) => {
                if (this.connected) {
                    this.socket.emit('drive', {
                        speed: pos.y * 100,  // Convert to -100 to 100 range
                        turn: pos.x * 100
                    });
                }
            }
        });

        // Steering joystick (right)
        this.steeringJoystick = new VirtualJoystick('steering-joystick', {
            size: 200,
            maxDistance: 75,
            onChange: (pos) => {
                if (this.connected) {
                    this.socket.emit('steer', {
                        angle: pos.x * 90  // Convert to -90 to 90 range
                    });
                }
            }
        });
    }

    setupControls() {
        // Emergency stop button
        document.getElementById('emergency-stop').addEventListener('click', () => {
            if (this.connected) {
                this.socket.emit('emergency_stop');
                this.updateStatus('Emergency Stop Activated', 'warning');
            }
        });
    }

    updateBatteryStatus(status) {
        const batteryLevel = document.getElementById('battery-level');
        const batteryVoltage = document.getElementById('battery-voltage');

        // Update battery level indicator
        batteryLevel.style.width = `${status.percentage}%`;
        batteryLevel.textContent = `${status.percentage}%`;
        batteryVoltage.textContent = `${status.voltage}V`;

        // Update color based on status
        batteryLevel.className = 'progress-bar';
        if (status.is_critical) {
            batteryLevel.classList.add('bg-danger');
        } else if (status.is_low) {
            batteryLevel.classList.add('bg-warning');
        } else {
            batteryLevel.classList.add('bg-success');
        }
    }

    showBatteryAlert(alert) {
        const alertElement = document.getElementById('battery-alert');
        alertElement.textContent = alert.message;
        alertElement.className = `alert alert-${alert.level} mt-3`;
        alertElement.classList.remove('d-none');
    }

    updateStatus(message, type) {
        const statusElement = document.getElementById('connection-status');
        statusElement.textContent = message;
        statusElement.className = `alert alert-${type}`;
    }
}

// Initialize controller when page loads
document.addEventListener('DOMContentLoaded', () => {
    const controller = new RobotController();
});