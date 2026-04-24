#!/bin/bash

set -e

echo "Updating system..."
sudo apt update
sudo apt install -y python3-pip git fonts-dejavu imagemagick

echo "Enabling SPI..."
sudo raspi-config nonint do_spi 0

echo "Installing Python deps..."
pip3 install -r requirements.txt

echo "Installing Waveshare library..."
if [ ! -d "e-Paper" ]; then
    git clone https://github.com/waveshare/e-Paper.git
fi

cd e-Paper/RaspberryPi_JetsonNano/python
pip3 install .
cd ../../../..

echo "Setting up systemd service..."
sudo cp service/trainboard.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl enable trainboard.service

echo "Done! Reboot to start."
