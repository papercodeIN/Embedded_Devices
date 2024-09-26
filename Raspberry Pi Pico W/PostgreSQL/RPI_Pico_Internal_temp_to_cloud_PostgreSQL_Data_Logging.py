import network  # Handles the Wi-Fi connection
import micropg_lite
import machine
import time

### Updated Wi-Fi connection data
ssid = 'Capgemini_4G'  # Replace with your Wi-Fi SSID
password = 'MN704116'  # Replace with your Wi-Fi password

# Connect to the network
print("Connecting to Wi-Fi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection
while not wlan.isconnected():
    time.sleep(1)

print("Wi-Fi connected:", wlan.ifconfig())

# Connect to PostgreSQL
print("Connecting to PostgreSQL database...")
try:
    conn = micropg_lite.connect(
        host='3.87.44.34',  # Replace with your server IP address
        user='myuser',  # Replace with your username
        password='mypassword',  # Replace with your password
        database='mydatabase'
    )
    print("Database connection successful.")
except Exception as e:
    print("Database connection failed:", e)
    raise

cur = conn.cursor()

# Function to read internal temperature
def read_internal_temperature():
    print("Reading internal temperature...")
    adc = machine.ADC(4)  # Internal temperature sensor is usually on GPIO 4
    raw_value = adc.read_u16()  # Read raw value (0-65535)
    
    # Convert raw value to temperature in Celsius
    temperature = (raw_value / 65535) * 3.3  # Convert to voltage (0 to 3.3V)
    temperature = (temperature - 0.5) * 100  # Convert to Celsius (0.5V corresponds to 0°C)
    
    print(f"Raw value: {raw_value}, Temperature: {temperature:.2f}°C")
    return round(temperature, 2)

# Loop to insert temperature data every 10 seconds
try:
    while True:
        # Read internal temperature
        temperature = read_internal_temperature()
        
        # Insert temperature into the sensor_data table
        print("Inserting temperature data into the database...")
        try:
            # Convert temperature to string before inserting
            cur.execute('INSERT INTO sensor_data (temperature) VALUES (%s)', (str(temperature),))
            conn.commit()
            print(f"Inserted temperature: {temperature:.2f}°C")
        except Exception as e:
            print("Error inserting data:", e)

        # Wait for 10 seconds before the next reading
        time.sleep(10)

except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    conn.close()
    print("Connection closed.")

