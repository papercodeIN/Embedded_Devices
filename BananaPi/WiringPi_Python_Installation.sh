#!/bin/bash

# Check current system date and time
echo "==============================="
echo "Checking current system date and time..."
echo "==============================="
date

# Synchronize system time with NTP
echo "==============================="
echo "Synchronizing system time with NTP..."
echo "==============================="
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd

# Install ntpdate for time synchronization
echo "==============================="
echo "Installing ntpdate for time synchronization..."
echo "==============================="
sudo apt-get install -y ntpdate

# Sync time with pool.ntp.org
echo "==============================="
echo "Syncing time with pool.ntp.org..."
echo "==============================="
sudo ntpdate pool.ntp.org

# Display updated system date and time
echo "==============================="
echo "Updated system date and time:"
echo "==============================="
date

# Update the package lists
echo "==============================="
echo "Updating package lists..."
echo "==============================="
sudo apt-get update

# Update and upgrade the system
echo "==============================="
echo "Updating and upgrading the system..."
echo "==============================="
sudo apt update && sudo apt upgrade -y

# Install necessary packages
echo "==============================="
echo "Installing required packages..."
echo "==============================="
sudo apt install -y build-essential python3-dev python3-setuptools swig git gettext-base fakeroot

# Clone the WiringPi-Python repository
echo "==============================="
echo "Cloning WiringPi-Python repository..."
echo "==============================="
git clone --recursive https://github.com/Dangku/WiringPi-Python.git

# Navigate to the WiringPi-Python directory
cd WiringPi-Python

# Install WiringPi-Python
echo "==============================="
echo "Installing WiringPi-Python..."
echo "==============================="
sudo python3 setup.py install

# Return to the root directory
echo "==============================="
echo "Returning to the root directory..."
echo "==============================="
cd ~

# Remove the WiringPi-Python directory
echo "==============================="
echo "Deleting the WiringPi-Python directory..."
echo "==============================="
rm -rf WiringPi-Python

echo "==============================="
echo "WiringPi installation completed successfully, and the directory has been deleted."
echo "==============================="