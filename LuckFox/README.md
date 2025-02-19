# **Environment Details**

## **Luckfox Pico Mini B / Pico Pro / Pico Max / Ultra W**

### **Ubuntu Machine**
- **Login:** pico  
- **Password:** luckfox  
- **Static IP:** 172.32.0.70  
- **SSH Login:**  
    ```bash
    ssh pico@172.32.0.70
    ```

### **Buildroot Machine**
- **Login:** root  
- **Password:** luckfox  
- **Static IP:** 172.32.0.93  
- **SSH Login:**  
    ```bash
    ssh root@172.32.0.93
    ```

---

## **Luckfox Lyra**

### **Buildroot OS**
- **Username:** root  
- **Password:** luckfox  
- **USB Static IP Address:** 192.168.123.100  
- **SSH Login:**  
    ```bash
    ssh root@192.168.123.100
    ```

### **Ubuntu OS**
- **Username:** lyra  
- **Password:** luckfox  
- **USB Static IP Address:** 192.168.123.100  
- **SSH Login:**  
    ```bash
    ssh lyra@192.168.123.100
    ```
---

# **Wi-Fi Setup on Ubuntu (Luckfox Pico Ultra W)**

### **List Available Wi-Fi Networks**
```bash
nmcli dev wifi list
```

### **Connect to a Wi-Fi Network**
```bash
sudo nmcli --ask dev wifi connect <network-ssid>
```
**Example:**  
```bash
sudo nmcli --ask dev wifi connect Capgemini_4G
```

---

# **Wi-Fi Hotspot Setup Using `nmcli`**

### **1. Create a Wi-Fi Hotspot**
```bash
nmcli d wifi hotspot ifname <wifi_interface> ssid <network_name> password <password>
```
**Example:**  
```bash
nmcli d wifi hotspot ifname wlan0 ssid luckfox_ap password 12345678
```
This creates a Wi-Fi hotspot named `luckfox_ap` on interface `wlan0` with the password `12345678`.

### **2. Display the Wi-Fi Hotspot Password**
```bash
nmcli dev wifi show-password
```

---

# **Clear SSH Entries on Windows**
To clear all SSH known hosts entries:  
```cmd
echo. > %userprofile%\.ssh\known_hosts
```

---

# **Check CPU Details on Buildroot OS**

To check CPU details, use the following commands:

```sh
cat /proc/cpuinfo
```

```sh
uname -a
```

---

# **Install Mosquitto on Luckfox Pico Ultra W**

## **1️⃣ Download & Run the Script**  
Run the following commands:  

```bash
wget https://raw.githubusercontent.com/papercodeIN/Embedded_Devices/refs/heads/main/LuckFox/Script/install_mosquitto.sh
chmod +x install_mosquitto.sh
./install_mosquitto.sh
```

## **2️⃣ Check Mosquitto Status**  
```bash
systemctl status mosquitto
```

## **3️⃣ Start/Stop/Restart Mosquitto**  
- **Start:** `sudo systemctl start mosquitto`  
- **Stop:** `sudo systemctl stop mosquitto`  
- **Restart:** `sudo systemctl restart mosquitto`  

## **4️⃣ Test Mosquitto**  
- **Subscribe:**  
  ```bash
  mosquitto_sub -h localhost -t test/topic
  ```
- **Publish:**  
  ```bash
  mosquitto_pub -h localhost -t test/topic -m "Hello, MQTT!"
  ```

If working, you'll see **"Hello, MQTT!"** in the subscriber terminal. ✅  

🎉 **Done! Mosquitto is installed and running!** 🚀

---

# **Install Node-RED and Node.js (Ubuntu)**

### **One-Step Installation**
```bash
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
```

---

# **File Transfer Using `scp`**

### **1. Transfer a ZIP File**
```bash
scp python-periphery-master.zip pico@172.32.0.70:/home/pico
```

### **2. Transfer a Directory**
```bash
scp -r python-periphery-master pico@172.32.0.70:/home/pico
```

---

# **Install Python Library (Ubuntu)**
## Option 1
### **1. Navigate to the Transferred Directory**
```bash
cd python-periphery-master
```

### **2. Install the Python Library**
```bash
sudo python3 setup.py install
```
## Option 2
```bash
pip install python-periphery
```
---

# **Control GPIO Using `periphery` in Python**

### **1. Open Python 3**
```bash
sudo python3
```

### **2. Control GPIO Pins**
```python
from periphery import GPIO

# GPIO pin number
Write_Pin = 41
Write_GPIO = GPIO(Write_Pin, "out")

# Set GPIO pin high
Write_GPIO.write(True)

# Set GPIO pin low
Write_GPIO.write(False)
```

---
