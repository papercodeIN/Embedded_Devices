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
   wget https://raw.githubusercontent.com/papercodeIN/Embedded_Devices/main/BananaPi/Node_RED_Installation.sh
   ```

2. **Make the Script Executable:**  
   ```bash
   chmod +x Node_RED_Installation.sh
   ```

3. **Run the Installation Script:**  
   ```bash
   ./Node_RED_Installation.sh
   ```

Got it! Here’s how you can incorporate the LED blink code into the steps for WiringPi installation and control the GPIO pins.

---

## **WiringPi Installation and LED Blink Code**

1. **Download the Installation Script:**
   ```bash
   wget https://raw.githubusercontent.com/papercodeIN/Embedded_Devices/main/BananaPi/WiringPi_Installation.sh
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

5. **Set GPIO Pin 7 as Output:**
   ```bash
   gpio mode 2 out
   ```

6. **Turn the LED On:**
   ```bash
   gpio write 7 1
   ```

7. **Turn the LED Off:**
   ```bash
   gpio write 7 0
   ```

---

This will make your LED blink 10 times with an interval of 1 second. If you need any more help, feel free to ask!

## **WiringPi-Python Installation**
1. **Download the Installation Script:**  
   ```bash
   wget https://raw.githubusercontent.com/papercodeIN/Embedded_Devices/refs/heads/main/BananaPi/WiringPi_Python_Installation.sh

   ```

2. **Make the Script Executable:**  
   ```bash
   chmod +x WiringPi_Python_Installation.sh
   ```

3. **Run the Installation Script:**  
   ```bash
   ./WiringPi_Python_Installation.sh
   ```
4. **Verify WiringPi-Python Installation using Blink Python Code:**  
   ```bash
   wget https://raw.githubusercontent.com/papercodeIN/Embedded_Devices/refs/heads/main/BananaPi/led_blink.py
   ```
   ### Change Pin Number as per your setup
   ```bash
   python3 led_blink.py
   ```   
---

## **Banana Pi YouTube Playlist Links**
Explore detailed tutorials for different Banana Pi models:

- 📺 **[Banana Pi BPI-P2 Pro YouTube Playlist](https://www.youtube.com/playlist?list=PLxrSjjYyzaaJf7wXYRMxTi6N13cYAuab-)**  
- 📺 **[Banana Pi BPI-M4 Berry YouTube Playlist](https://www.youtube.com/playlist?list=PLxrSjjYyzaaJXDh-iKOQY-EMEp0uqdyD2)**  
- 📺 **[Banana Pi BPI-M4 Zero YouTube Playlist](https://www.youtube.com/playlist?list=PLxrSjjYyzaaJ4cOlBL80YnnAXfSN2oSzT)**  

---

## M4 Berry 
```
root@bpi-m4berry:~# gpio readall
 +-----+-----+---------+------+---+ M4 Berry +---+------+---------+-----+-----+
 | I/O | wPi |   Name  | Mode | V | Physical | V | Mode |  Name   | wPi | I/O |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3V |      |   |  1 || 2  |   |      | 5V      |     |     |
 | 208 |   8 |   SDA.4 |   IN | 1 |  3 || 4  |   |      | 5V      |     |     |
 | 207 |   9 |   SCL.4 |   IN | 1 |  5 || 6  |   |      | 0V      |     |     |
 | 211 |   7 |  IO.211 | ALT7 | 0 |  7 || 8  | 0 | ALT2 | TxD1    | 15  | 198 |
 |     |     |      0V |      |   |  9 || 10 | 0 | ALT2 | RxD1    | 16  | 199 |
 | 226 |   0 |  IO.226 | ALT7 | 0 | 11 || 12 | 0 | ALT7 | IO.203  | 1   | 203 |
 | 227 |   2 |  IO.227 | ALT7 | 0 | 13 || 14 |   |      | 0V      |     |     |
 | 194 |   3 |  IO.194 | ALT7 | 0 | 15 || 16 | 0 | ALT2 | IO.200  | 4   | 200 |
 |     |     |    3.3V |      |   | 17 || 18 | 0 | ALT2 | IO.201  | 5   | 201 |
 | 231 |  12 |    MOSI | ALT4 | 0 | 19 || 20 |   |      | 0V      |     |     |
 | 232 |  13 |    MISO | ALT4 | 0 | 21 || 22 | 0 | ALT7 | IO.193  | 6   | 193 |
 | 230 |  14 |    SLCK | ALT4 | 0 | 23 || 24 | 0 | ALT4 | SS      | 10  | 229 |
 |     |     |      0V |      |   | 25 || 26 | 0 | ALT4 | IO.233  | 11  | 233 |
 | 210 |  30 |   SDA.3 | ALT7 | 0 | 27 || 28 | 0 | ALT7 | SCL.3   | 31  | 209 |
 | 195 |  21 |  IO.195 | ALT7 | 0 | 29 || 30 |   |      | 0V      |     |     |
 | 196 |  22 |  IO.196 | ALT7 | 0 | 31 || 32 | 0 | ALT7 | IO.192  | 26  | 192 |
 | 197 |  23 |  IO.197 | ALT7 | 0 | 33 || 34 |   |      | 0V      |     |     |
 | 204 |  24 |  IO.204 | ALT7 | 0 | 35 || 36 | 0 | ALT7 | IO.228  | 27  | 228 |
 | 202 |  25 |  IO.202 | ALT7 | 0 | 37 || 38 | 0 | ALT7 | IO.206  | 28  | 206 |
 |     |     |      0V |      |   | 39 || 40 | 0 | ALT7 | IO.205  | 29  | 205 |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | I/O | wPi |   Name  | Mode | V | Physical | V | Mode |  Name   | wPi | I/O |
 +-----+-----+---------+------+---+ M4 Berry +---+------+---------+-----+-----+
```

## M4 Zero
```
root@bpi-m4zero:~# gpio readall
 +-----+-----+---------+------+---+- M4Zero -+---+------+---------+-----+-----+
 | I/O | wPi |   Name  | Mode | V | Physical | V | Mode |  Name   | wPi | I/O |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3V |      |   |  1 || 2  |   |      | 5V      |     |     |
 | 262 |   8 |   SDA.0 |   IN | 1 |  3 || 4  |   |      | 5V      |     |     |
 | 261 |   9 |   SCL.0 |   IN | 1 |  5 || 6  |   |      | 0V      |     |     |
 | 268 |   7 |  IO.268 |  OUT | 0 |  7 || 8  | 0 | ALT3 | TxD1    | 15  | 269 |
 |     |     |      0V |      |   |  9 || 10 | 0 | ALT3 | RxD1    | 16  | 270 |
 | 226 |   0 |  IO.226 | ALT7 | 0 | 11 || 12 | 0 | ALT7 | IO.257  | 1   | 257 |
 | 227 |   2 |  IO.227 |  OUT | 0 | 13 || 14 |   |      | 0V      |     |     |
 | 267 |   3 |  IO.267 | ALT7 | 0 | 15 || 16 | 0 | ALT3 | IO.271  | 4   | 271 |
 |     |     |    3.3V |      |   | 17 || 18 | 0 | ALT3 | IO.272  | 5   | 272 |
 | 231 |  12 |    MOSI | ALT4 | 0 | 19 || 20 |   |      | 0V      |     |     |
 | 232 |  13 |    MISO | ALT4 | 0 | 21 || 22 | 0 | ALT7 | IO.66   | 6   | 66  |
 | 230 |  14 |    SLCK | ALT4 | 0 | 23 || 24 | 0 | ALT4 | SS      | 10  | 229 |
 |     |     |      0V |      |   | 25 || 26 | 0 | ALT4 | IO.233  | 11  | 233 |
 | 264 |  30 |   SDA.1 | ALT7 | 0 | 27 || 28 | 0 | ALT7 | SCL.1   | 31  | 263 |
 | 266 |  21 |  IO.266 | ALT7 | 0 | 29 || 30 |   |      | 0V      |     |     |
 | 265 |  22 |  IO.265 | ALT7 | 0 | 31 || 32 | 0 | ALT7 | IO.228  | 26  | 228 |
 | 234 |  23 |  IO.234 | ALT3 | 0 | 33 || 34 |   |      | 0V      |     |     |
 | 258 |  24 |  IO.258 | ALT7 | 0 | 35 || 36 | 0 | ALT7 | IO.71   | 27  | 71  |
 | 256 |  25 |  IO.256 | ALT7 | 0 | 37 || 38 | 0 | ALT7 | IO.260  | 28  | 260 |
 |     |     |      0V |      |   | 39 || 40 | 0 | ALT7 | IO.259  | 29  | 259 |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | I/O | wPi |   Name  | Mode | V | Physical | V | Mode |  Name   | wPi | I/O |
 +-----+-----+---------+------+---+- M4Zero -+---+------+---------+-----+-----+
```