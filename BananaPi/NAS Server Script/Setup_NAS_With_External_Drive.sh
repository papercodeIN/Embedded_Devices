#!/bin/bash

# Synchronize System Time
echo "==============================="
echo "Enabling NTP and synchronizing system time..."
echo "==============================="
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd

echo "==============================="
echo "Installing ntpdate..."
echo "==============================="
sudo apt install -y ntpdate
sudo ntpdate pool.ntp.org

echo "==============================="
echo "Time synchronization completed."
echo "==============================="

# Update and Upgrade the System
echo "==============================="
echo "Updating and upgrading the system..."
echo "==============================="
sudo apt-get update && sudo apt-get upgrade -y

# Install Necessary Packages
echo "==============================="
echo "Installing required packages..."
echo "==============================="
sudo apt-get install -y samba ntfs-3g

# Verify Samba Installation
echo "==============================="
echo "Verifying Samba installation..."
echo "==============================="
whereis samba

# Create Directory for NAS
echo "==============================="
echo "Creating NAS directory..."
echo "==============================="
mkdir -p /home/pi/NAS

# Prepare NTFS Drive
echo "==============================="
echo "Preparing NTFS drive..."
echo "==============================="
sudo blkid /dev/sda

fs_type=$(blkid -s TYPE -o value /dev/sda)
if [ "$fs_type" != "ntfs" ]; then
    echo "Error: /dev/sda is not an NTFS filesystem. Exiting..."
    exit 1
fi

mount | grep /dev/sda

echo "==============================="
echo "Unmounting the drive if already mounted..."
echo "==============================="
if mount | grep -q /dev/sda; then
    sudo umount /dev/sda
    sudo fuser -v /dev/sda
    sudo umount -f /dev/sda
fi

echo "==============================="
echo "Checking for existing fstab entry..."
echo "==============================="
cat /etc/fstab | grep /dev/sda

echo "==============================="
echo "Mounting the NTFS drive..."
echo "==============================="
sudo mount -t ntfs-3g -o rw /dev/sda /home/pi/NAS

# Add to fstab for persistent mounting
UUID=$(blkid -s UUID -o value /dev/sda)
echo "UUID=$UUID /home/pi/NAS ntfs-3g rw,defaults 0 0" | sudo tee -a /etc/fstab

# Edit Samba Configuration
echo "==============================="
echo "Configuring Samba..."
echo "==============================="
sudo bash -c 'cat >> /etc/samba/smb.conf <<EOL

[NAS SERVER]
comment = Banana Pi NAS SERVER
path = /home/pi/NAS
read only = no
browsable = yes

EOL'

# Restart Samba Service
echo "==============================="
echo "Restarting Samba service..."
echo "==============================="
sudo service smbd restart

# Test Samba Configuration
sudo testparm

# Set Samba Password for Root User
echo "==============================="
echo "Setting Samba password for the root user..."
echo "==============================="
echo -e "toor\ntoor" | sudo smbpasswd -s -a root

# Get the Banana Pi IP Address
echo "==============================="
echo "Fetching Banana Pi IP address..."
echo "==============================="
NAS_IP=$(hostname -I | awk '{print $1}')

# Samba Default Port
SAMBA_PORT=445

# Display IP and Port Information
echo "==============================="
echo "Samba NAS Server Setup Complete!"
echo "Access your NAS server using the following details:"
echo "IP Address: $NAS_IP"
echo "Port: $SAMBA_PORT"
echo "You can access the shared folder via \\\\$NAS_IP\\NAS SERVER\\ in your file explorer (Windows/Linux)."
echo "==============================="
