#!/bin/bash

# Check current system date and time
echo "Checking current system date and time..."
date

# Synchronize system time with NTP
echo "Synchronizing system time with NTP..."
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd

# Install ntpdate for time synchronization
echo "Installing ntpdate for time synchronization..."
sudo apt-get install -y ntpdate

# Sync time with pool.ntp.org
echo "Syncing time with pool.ntp.org..."
sudo ntpdate pool.ntp.org

# Display updated system date and time
echo "Updated system date and time:"
date

# Update the package lists
echo "Updating package lists..."
sudo apt-get update

# Update and upgrade the system
echo "Updating and upgrading the system..."
sudo apt update && sudo apt upgrade -y

# Install necessary packages
echo "Installing required packages..."
sudo apt install -y build-essential python3-dev python3-setuptools swig git gettext-base fakeroot

# Clone the WiringPi-Python repository
echo "Cloning WiringPi-Python repository..."
git clone --recursive https://github.com/Dangku/WiringPi-Python.git

# Navigate to the WiringPi-Python directory
cd WiringPi-Python

# Install WiringPi-Python
echo "Installing WiringPi-Python..."
sudo python3 setup.py install

# Return to the root directory
echo "Returning to the root directory..."
cd ~

# Remove the WiringPi-Python directory
echo "Deleting the WiringPi-Python directory..."
rm -rf WiringPi-Python

echo "WiringPi installation completed successfully, and the directory has been deleted."