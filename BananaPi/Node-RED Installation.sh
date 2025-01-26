#!/bin/bash

# Install Node-RED
# curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
# sudo apt-get install -y nodejs
# sudo apt-get install npm
# sudo npm install -g --unsafe-perm node-red
# node-red

# Function to check and correct system date and time
check_and_correct_time() {
  echo "Checking current system date and time..."
  date

  echo "Synchronizing system time with NTP..."
  sudo timedatectl set-ntp true
  sudo systemctl restart systemd-timesyncd

  echo "Installing ntpdate for time synchronization..."
  sudo apt-get install -y ntpdate

  echo "Syncing time with pool.ntp.org..."
  sudo ntpdate pool.ntp.org

  echo "Updated system date and time:"
  date
}

# Function to install Node-RED
install_node_red() {
  echo "Installing Node-RED..."
  bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
}

# Main script execution
echo "Starting setup..."

# Check and correct time
check_and_correct_time

# Install Node-RED
install_node_red

echo "Setup completed! Node-RED is ready to use."
