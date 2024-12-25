try:
    from picamera import PiCamera
except ImportError:
    from hardware.mock_picamera import PiCamera
import io
import logging
import threading
import time
from config import CAMERA_RESOLUTION, CAMERA_FRAMERATE, CAMERA_ROTATION

class CameraStream:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = CAMERA_RESOLUTION
        self.camera.framerate = CAMERA_FRAMERATE
        self.camera.rotation = CAMERA_ROTATION
        self.output = io.BytesIO()
        self.frame = None
        self.stopped = False
        logging.debug("Camera stream initialized")

    def start(self):
        """Start the camera stream thread"""
        threading.Thread(target=self._update, daemon=True).start()
        return self

    def _update(self):
        """Continuously capture frames from the camera"""
        for _ in self.camera.capture_continuous(self.output, format='jpeg', use_video_port=True):
            if self.stopped:
                return

            self.frame = self.output.getvalue()
            self.output.seek(0)
            self.output.truncate()
            time.sleep(1/CAMERA_FRAMERATE)

    def read(self):
        """Return the most recent frame"""
        return self.frame

    def stop(self):
        """Stop the camera stream"""
        self.stopped = True
        self.camera.close()