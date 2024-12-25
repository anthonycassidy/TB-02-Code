"""Mock PiCamera module for development environment"""
import io
import logging
import time
from PIL import Image

class PiCamera:
    def __init__(self):
        self.resolution = (640, 480)
        self.framerate = 24
        self.rotation = 0
        self._mock_frame = self._create_mock_frame()
        logging.debug("Mock PiCamera initialized")

    def _create_mock_frame(self):
        """Create a mock frame with text indicating it's a development preview"""
        img = Image.new('RGB', self.resolution, color='darkgray')
        return img

    def capture_continuous(self, output, format='jpeg', use_video_port=False):
        """Simulate continuous capture by yielding mock frames"""
        while True:
            # Save mock frame to the output stream
            output.seek(0)
            self._mock_frame.save(output, format='JPEG')
            yield output
            time.sleep(1.0 / self.framerate)

    def close(self):
        logging.debug("Mock PiCamera closed")
