# Update system packages
sudo apt update
sudo apt upgrade -y

# Install required system dependencies
sudo apt install -y python3-pip python3-venv git
sudo apt install -y python3-picamera2 python3-libcamera
sudo apt install -y i2c-tools python3-smbus

# Enable required interfaces
sudo raspi-config nonint do_camera 0
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0