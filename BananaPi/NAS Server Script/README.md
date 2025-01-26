## Step 1: Check Attached Storage Devices
To view the storage devices available on your system, use the following command:
```bash
lsblk
```
This command lists all block devices, including internal and external drives, their mount points, and partitions. Use this information to identify the storage drive(s) you want to use for your NAS setup.

---

## Step 2: Setting Up a NAS Storage Server

### **Option A: Using Internal Storage**
1. Create the setup script:
   ```bash
   nano Setup_NAS.sh
   ```
2. Write the required configuration in `Setup_NAS.sh` for setting up the NAS server.  
   Example: Define network shares, set permissions, and configure SMB/CIFS or NFS services.

3. Make the script executable:
   ```bash
   chmod +x Setup_NAS.sh
   ```
4. Run the setup script:
   ```bash
   ./Setup_NAS.sh
   ```

### **Option B: Using an External Storage Drive**
1. Create the setup script:
   ```bash
   nano Setup_NAS_With_External_Drive.sh
   ```
2. Write the required configuration in `Setup_NAS_With_External_Drive.sh` for setting up the NAS server with an external drive.  
   Example: Mount the external drive, configure network shares, set permissions, and configure services.

3. Make the script executable:
   ```bash
   chmod +x Setup_NAS_With_External_Drive.sh
   ```
4. Run the setup script:
   ```bash
   ./Setup_NAS_With_External_Drive.sh
   ```
