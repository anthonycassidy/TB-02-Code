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
