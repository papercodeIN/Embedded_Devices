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

# Install Node-RED
echo "Installing Node-RED..."
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

echo "Setup completed! Node-RED is ready to use."
