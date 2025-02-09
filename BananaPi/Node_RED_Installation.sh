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

# Install Node-RED
echo "==============================="
echo "Installing Node-RED..."
echo "==============================="
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

echo "==============================="
echo "Setup completed! Node-RED is ready to use."
echo "==============================="
