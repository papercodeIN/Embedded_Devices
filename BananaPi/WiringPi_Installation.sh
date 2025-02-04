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

# Install required packages including build-essential
echo "Installing required packages..."
sudo apt install -y build-essential python3-dev python3-setuptools swig git gettext-base fakeroot

# Fetch the source
echo "Installing dependencies and fetching source..."
git clone https://github.com/Dangku/WiringPi.git
cd WiringPi

# Build the package
echo "Building the WiringPi package..."
./build debian
mv debian-template/wiringpi_3.6_arm64.deb /tmp/

# Install the package
echo "Installing WiringPi package..."
sudo apt install -y /tmp/wiringpi_3.6_arm64.deb

# Return to the parent directory and remove the WiringPi folder
cd ..
echo "Cleaning up: Removing WiringPi directory..."
rm -rf WiringPi

echo "Script completed successfully, and the WiringPi directory has been deleted."
