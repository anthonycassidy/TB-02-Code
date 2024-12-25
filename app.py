try:
    import RPi.GPIO as GPIO
except ImportError:
    import hardware.mock_gpio as GPIO
from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import logging
from hardware.motor_controller import MotorController
from hardware.servo_controller import ServoController
from hardware.camera_stream import CameraStream

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'robotcontrol2024'
socketio = SocketIO(app)

# Initialize hardware controllers
motor_controller = MotorController()
servo_controller = ServoController()
camera_stream = CameraStream().start()

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    """Generate camera frames for streaming"""
    while True:
        frame = camera_stream.read()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect')
def handle_connect():
    logging.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    logging.info('Client disconnected')
    motor_controller.stop()
    servo_controller.center_all()

@socketio.on('drive')
def handle_drive(data):
    """Handle drive joystick input"""
    try:
        speed = data['speed']
        turn = data['turn']

        # Implement differential drive
        left_speed = speed + turn
        right_speed = speed - turn

        # Normalize speeds
        max_speed = max(abs(left_speed), abs(right_speed), 100)
        if max_speed > 100:
            left_speed = (left_speed * 100) / max_speed
            right_speed = (right_speed * 100) / max_speed

        motor_controller.set_speed(left_speed)
        logging.debug(f'Drive command: speed={speed}, turn={turn}')
    except Exception as e:
        logging.error(f'Error in drive command: {e}')

@socketio.on('steer')
def handle_steer(data):
    """Handle steering joystick input"""
    try:
        angle = data['angle']
        for servo in ['FRONT_LEFT', 'FRONT_RIGHT', 'REAR_LEFT', 'REAR_RIGHT']:
            servo_controller.set_angle(servo, 90 + angle)
        logging.debug(f'Steer command: angle={angle}')
    except Exception as e:
        logging.error(f'Error in steer command: {e}')

@socketio.on('emergency_stop')
def handle_emergency_stop():
    """Handle emergency stop button"""
    try:
        motor_controller.stop()
        servo_controller.center_all()
        logging.info('Emergency stop activated')
    except Exception as e:
        logging.error(f'Error in emergency stop: {e}')

@app.errorhandler(Exception)
def handle_error(error):
    logging.error(f'Unhandled error: {error}')
    return str(error), 500

def cleanup():
    """Cleanup GPIO and camera resources"""
    camera_stream.stop()
    motor_controller.cleanup()
    servo_controller.cleanup()
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    finally:
        cleanup()