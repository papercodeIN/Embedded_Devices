#!/bin/bash

# Synchronize System Time
echo "Enabling NTP and synchronizing system time..."
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
echo "Installing ntpdate..."
sudo apt install -y ntpdate
sudo ntpdate pool.ntp.org
echo "Time synchronization completed."

# Update and Upgrade the System
echo "Updating and upgrading the system..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Samba
echo "Installing Samba..."
sudo apt install -y samba

# Verify Samba Installation
echo "Verifying Samba installation..."
whereis samba

# Create Directory for NAS
echo "Creating NAS directory..."
mkdir -p /home/pi/NAS

# Edit Samba Configuration
echo "Configuring Samba..."
sudo bash -c 'cat >> /etc/samba/smb.conf <<EOL

[NAS SERVER]
comment = Banana Pi NAS SERVER
path = /home/pi/NAS
read only = no
browsable = yes

EOL'

# Restart Samba Service
echo "Restarting Samba service..."
sudo service smbd restart

# Set Samba Password for Root User
echo "Setting Samba password for the root user..."
echo -e "toor\ntoor" | sudo smbpasswd -s -a root

# Get the Banana Pi IP Address
echo "Fetching Banana Pi IP address..."
NAS_IP=$(hostname -I | awk '{print $1}')

# Samba Default Port
SAMBA_PORT=445

# Display IP and Port Information
echo "Samba NAS Server Setup Complete!"
echo "Access your NAS server using the following details:"
echo "IP Address: $NAS_IP"
echo "Port: $SAMBA_PORT"
echo "You can access the shared folder via \\$NAS_IP\\nas server\\ in your file explorer (Windows/Linux)."
