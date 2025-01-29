Banana Pi M4 Zero Documentation Page: https://wiki.banana-pi.org/Banana_Pi_BPI-M4_Zero
| OS                                    | Download Link                                                            | Release Date |
|---------------------------------------|--------------------------------------------------------------------------|--------------|
| Armbian based on Ubuntu 22.04         | https://drive.google.com/drive/folders/1-MzSVsduPX8qHKgbAOM3wmcCbwfkffAz | 2024-08-19   |
| Android 12                            | https://drive.google.com/file/d/1twgJpV4kbHkK-OKiEwhMCIxbnkIw74dF/view   | 2024-08-19   |
| Armbian based on Debian 12 (Bookworm) | https://drive.google.com/drive/folders/1Csk5mTyInOaWP6HsZbt_nk8V7dlG6Db0 | 2024-10-11   |
| Debian 12 (Bookworm)                  | https://drive.google.com/file/d/1OKrAm2fX8pLpiYM6GcQOIyNdcgQh9_bH/view   | 2024-03-14   |

---

# Banana Pi Setup Instructions  

## **Default Login Credentials**
- **Login Option 1:**  
  - **Username:** pi  
  - **Password:** bananapi  

- **Login Option 2:**  
  - **Username:** root  
  - **Password:** bananapi  

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

## **Install Armbian**
To install Armbian on Banana Pi:
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

---
