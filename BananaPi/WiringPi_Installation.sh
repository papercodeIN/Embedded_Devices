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

# Install required packages including build-essential
echo "==============================="
echo "Installing required packages..."
echo "==============================="
sudo apt install -y build-essential python3-dev python3-setuptools swig git gettext-base fakeroot

# Fetch the source
echo "==============================="
echo "Installing dependencies and fetching source..."
echo "==============================="
git clone https://github.com/Dangku/WiringPi.git
cd WiringPi

# Build the package
echo "==============================="
echo "Building the WiringPi package..."
echo "==============================="
./build debian
mv debian-template/wiringpi_3.6_arm64.deb /tmp/

# Install the package
echo "==============================="
echo "Installing WiringPi package..."
echo "==============================="
sudo apt install -y /tmp/wiringpi_3.6_arm64.deb

# Return to the parent directory and remove the WiringPi folder
cd ..
echo "==============================="
echo "Cleaning up: Removing WiringPi directory..."
echo "==============================="
rm -rf WiringPi

echo "==============================="
echo "Script completed successfully, and the WiringPi directory has been deleted."
echo "==============================="
