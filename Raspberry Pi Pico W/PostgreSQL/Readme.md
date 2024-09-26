## Create Table Query if Table do not Exists
```CREATE TABLE IF NOT EXISTS sensor_data (
        id SERIAL PRIMARY KEY,
        temperature FLOAT NOT NULL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )```