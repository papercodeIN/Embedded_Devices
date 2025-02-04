# **Banana Pi Setup Guide**

## **Default Login Credentials**
Below are the default login credentials based on your Banana Pi model:

| **Login Option** | **Username** | **Password** |
|-----------------|-------------|-------------|
| Option 1        | `pi`        | `bananapi`  |
| Option 2        | `root`      | `bananapi`  |
| Option 3 (P2-Pro) | `linaro`  | `linaro`    |

---

## **Connecting to Wi-Fi**
To connect your Banana Pi to a Wi-Fi network:

1. **List Available Wi-Fi Networks:**
   ```bash
   nmcli dev wifi list
   ```

2. **Connect to a Wi-Fi Network:**
   ```bash
   sudo nmcli --ask dev wifi connect <network-ssid>
   ```
   **Example:**  
   ```bash
   nmcli --ask dev wifi connect Capgemini_4G
   ```

---

## **Clear SSH Host Entries (Windows)**
If you encounter SSH fingerprint errors, clear the known hosts file:

```cmd
echo. > %userprofile%\.ssh\known_hosts
```

---

## **Armbian Setup**
To set up Armbian on Banana Pi:

```bash
sudo armbian-install
```

---

## **Disk Operations & Formatting**
### **1. List Available Storage Devices**
```bash
lsblk
```

### **2. Wipe the Entire Storage Device**
```bash
sudo dd if=/dev/zero of=/dev/mmcblk0 bs=4M status=progress
```

> **Note:** This will erase all data on the device. Ensure you've selected the correct block device.

### **3. Partition and Format Storage**
1. **Create New Partitions:**
   ```bash
   sudo fdisk /dev/mmcblk0
   ```
2. **Format Partition as ext4:**
   ```bash
   sudo mkfs.ext4 /dev/mmcblk0p1
   ```

---

## **Node-RED Installation**
1. **Download the Installation Script:**  
   ```bash
   wget https://github.com/papercodeIN/Embedded_Devices/blob/main/BananaPi/Node_RED_Installation.sh
   ```

2. **Make the Script Executable:**  
   ```bash
   chmod +x Node_RED_Installation.sh
   ```

3. **Run the Installation Script:**  
   ```bash
   ./Node_RED_Installation.sh
   ```

---

## **WiringPi Installation**
1. **Download the Installation Script:**  
   ```bash
   wget https://github.com/papercodeIN/Embedded_Devices/blob/main/BananaPi/WiringPi_Installation.sh
   ```

2. **Make the Script Executable:**  
   ```bash
   chmod +x WiringPi_Installation.sh
   ```

3. **Run the Installation Script:**  
   ```bash
   ./WiringPi_Installation.sh
   ```

4. **Verify WiringPi Installation:**  
   ```bash
   gpio readall
   ```

---

## **Banana Pi YouTube Playlist Links**
Explore detailed tutorials for different Banana Pi models:

- 📺 **[Banana Pi BPI-P2 Pro YouTube Playlist](https://www.youtube.com/playlist?list=PLxrSjjYyzaaJf7wXYRMxTi6N13cYAuab-)**  
- 📺 **[Banana Pi BPI-M4 Berry YouTube Playlist](https://www.youtube.com/playlist?list=PLxrSjjYyzaaJXDh-iKOQY-EMEp0uqdyD2)**  
- 📺 **[Banana Pi BPI-M4 Zero YouTube Playlist](https://www.youtube.com/playlist?list=PLxrSjjYyzaaJ4cOlBL80YnnAXfSN2oSzT)**  

---
