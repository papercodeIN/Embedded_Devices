#!/bin/bash

echo "==============================="
echo "Checking and synchronizing system time..."
echo "==============================="
date
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
sudo apt-get install -y ntpdate
sudo ntpdate pool.ntp.org
date

echo "==============================="
echo "Updating and upgrading the system..."
echo "==============================="
sudo apt-get update && sudo apt-get upgrade -y

echo "==============================="
echo "Installing required packages..."
echo "==============================="
sudo apt install -y build-essential python3-dev python3-setuptools swig git

echo "==============================="
echo "Cloning and installing RPi.GPIO..."
echo "==============================="
git clone https://github.com/Dangku/RPi.GPIO.git
cd RPi.GPIO
sudo python3 setup.py clean --all
sudo python3 setup.py build install
cd ..
rm -rf RPi.GPIO

echo "==============================="
echo "All tasks completed successfully!"
echo "==============================="