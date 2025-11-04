"""
Raspberry Pi Final Project
Author: Tomas King
This code interfaces with the Raspberry Pi and utilizes a DHT11 to take 
temperature and humidity readings there is conversion done for celsius to fahrenheit
and Kelvin just for fun.
The provided documentation for this sensor was outdated and this would have been impossible
without this helpful tutorial.
https://www.linkedin.com/pulse/how-read-temperature-your-raspberry-pi-5-jagrat-rao-wgpoc
"""
import time
import board
import adafruit_dht
from datetime import datetime
import csv

# DHT11 Sensor after D is GPIO pin number
dhtDevice = adafruit_dht.DHT11(board.D17)

# Open CSV file in append 'a' mode
with open('dht_sensor.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    while True:
        try:
            # timestamp for each entry
            timestamp = datetime.now().strftime('%H:%M:%S')
            # Date for each entry
            date = datetime.now().strftime('%Y-%m-%d')
            # Actual reading from the device are in celsius
            temp_c = dhtDevice.temperature
            # Some quick math to convert to fahrenheit
            temp_f = temp_c * (9 / 5) + 32
            # Conversion to Kelvin just for fun
            temp_k = temp_c + 273.15
            # Retrieve humidity reading from sensor
            humidity = dhtDevice.humidity
            # Write data to the file
            writer.writerow([timestamp, date, temp_f, temp_c, temp_k, humidity])
            # Bypass buffer and write to the CSV immediately rather than in batches
            f.flush()
            #Print to the console whats being written to the CSV
            print(
                "Timestamp: {} {} Temp: {:.1f} F / {:.1f} C / {:.1f} K   Humidity: {}%".format(
                    timestamp, date, temp_f, temp_c, temp_k, humidity
                )
            )
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        # Wait for a while before the next reading
        time.sleep(2.0)
