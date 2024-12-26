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

# Install Necessary Packages
echo "Installing required packages..."
sudo apt-get install -y samba ntfs-3g

# Verify Samba Installation
echo "Verifying Samba installation..."
whereis samba

# Create Directory for NAS
echo "Creating NAS directory..."
mkdir -p /home/pi/NAS

# Prepare NTFS Drive
echo "Preparing NTFS drive..."
sudo blkid /dev/sda

fs_type=$(blkid -s TYPE -o value /dev/sda)
if [ "$fs_type" != "ntfs" ]; then
    echo "Error: /dev/sda is not an NTFS filesystem. Exiting..."
    exit 1
fi

mount | grep /dev/sda

echo "Unmounting the drive if already mounted..."
if mount | grep -q /dev/sda; then
    sudo umount /dev/sda
    sudo fuser -v /dev/sda
    sudo umount -f /dev/sda
fi

echo "Checking for existing fstab entry..."
cat /etc/fstab | grep /dev/sda

echo "Mounting the NTFS drive..."
sudo mount -t ntfs-3g -o rw /dev/sda /home/pi/NAS

# Add to fstab for persistent mounting
UUID=$(blkid -s UUID -o value /dev/sda)
echo "UUID=$UUID /home/pi/NAS ntfs-3g rw,defaults 0 0" | sudo tee -a /etc/fstab

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

# Test Samba Configuration
sudo testparm

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
echo "You can access the shared folder via \\\\$NAS_IP\\NAS SERVER\\ in your file explorer (Windows/Linux)."
