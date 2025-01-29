## **Environment Details**
- **Ubuntu Machine**
  - **Login:** pico  
  - **Password:** luckfox  
  - **Static IP:** 172.32.0.70  
  - **SSH Login:**  
    ```bash
    ssh pico@172.32.0.70
    ```

- **Buildroot Machine**
  - **Login:** root  
  - **Password:** luckfox  
  - **Static IP:** 172.32.0.93  
  - **SSH Login:**  
    ```bash
    ssh root@172.32.0.93
    ```

---

## **Connect to WiFi on Ubuntu**
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
   sudo nmcli --ask dev wifi connect Capgemini_4G
   ```

---

## **Clear SSH Entries on a Windows Machine**
To clear all SSH known hosts entries:
```cmd
echo. > %userprofile%\.ssh\known_hosts
```

---

## **Install Node-RED and Node.js (Ubuntu)**
Execute the following command to install or update Node.js and Node-RED:  
```bash
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
```

---

## **Transfer Files Using `scp`**
1. **Transfer a ZIP file:**  
   ```bash
   scp python-periphery-master.zip pico@172.32.0.70:/home/pico
   ```
2. **Transfer a folder:**  
   ```bash
   scp -r python-periphery-master pico@172.32.0.70:/home/pico
   ```

---

## **Install Python Library (Ubuntu)**
1. Navigate to the transferred directory:
   ```bash
   cd python-periphery-master
   ```
2. Install the Python library:
   ```bash
   sudo python3 setup.py install
   ```

---

## **Control GPIO Using `periphery`**
1. Open Python 3:
   ```bash
   sudo python3
   ```
2. Execute the following commands to control GPIO pins:
   ```python
   from periphery import GPIO

   Write_Pin = 41
   Write_GPIO = GPIO(Write_Pin, "out")

   # Set GPIO pin high
   Write_GPIO.write(True)

   # Set GPIO pin low
   Write_GPIO.write(False)
   ```

---
