# Banana Pi Setup Instructions (Updated)

## **Default Login Credentials**
- **Login Option 1(Banana Pi M4-Berry & Banana Pi M4-Zero):**  
  - **Username:** pi  
  - **Password:** bananapi  

- **Login Option 2(Banana Pi M4-Berry & Banana Pi M4-Zero):**  
  - **Username:** root  
  - **Password:** bananapi  

- **Login Option 3 (Banana Pi P2-Pro):**  
  - **Username:** linaro  
  - **Password:** linaro  

---

## **Connect to Wi-Fi**
1. List available Wi-Fi networks:
   ```bash
   nmcli dev wifi list
   ```
2. Connect to a Wi-Fi network:
   ```bash
   sudo nmcli --ask dev wifi connect <network-ssid>
   ```
   Example:
   ```bash
   nmcli --ask dev wifi connect Capgemini_4G
   ```

---

## **Clear SSH Entries on a Windows Machine**
To clear all SSH known hosts entries:
```cmd
echo. > %userprofile%\.ssh\known_hosts
```

---

## **Setup Armbian**
To setup Armbian on Banana Pi:
```bash
sudo armbian-install
```

---

## **Disk Operations and Formatting**

### **Identify Storage Devices**
To list all block storage devices:
```bash
lsblk
```

### **Wipe Storage Device**
1. Wipe the entire storage device with zeroes:
   ```bash
   sudo dd if=/dev/zero of=/dev/mmcblk0
   ```
2. Alternatively, use a larger block size for faster operations:
   ```bash
   sudo dd if=/dev/zero of=/dev/mmcblk0 bs=4M status=progress
   ```

### **Partition and Format Storage**
1. Create partitions on the storage device:
   ```bash
   sudo fdisk /dev/mmcblk0
   ```
2. Format the partition to ext4:
   ```bash
   sudo mkfs.ext4 /dev/mmcblk1p1
   ```
