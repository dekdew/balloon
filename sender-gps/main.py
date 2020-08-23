import pycom
import time
import gc
import socket
from L76GNSS import L76GNSS
from pytrack import Pytrack
from network import LoRa
import ubinascii
import json

# Colors used for status LED
RGB_OFF = 0x000000
RGB_POS_UPDATE = 0x101000
RGB_POS_FOUND = 0x001000
RGB_POS_NFOUND = 0x100000
RGB_LORA = 0x000010
LED_TIMEOUT = 0.2
pycom.heartbeat(False)

# Set up the LoRa in longer range mode

lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
DevEUI = ubinascii.hexlify(lora.mac()).decode('ascii')

# Enable garbage collection

time.sleep(2)
gc.enable()

# Set up GPS with modest timeout

py = Pytrack()
l76 = L76GNSS(py)

last_lat = 13.736717
last_lon = 100.523186
last_alt = 0

while True:
    try:  
        battery = py.read_battery_voltage()  # Get battery
        gps = l76.gps_message('GGA')  # Gets coordinates


        lat = gps["Latitude"]
        lon = gps["Longitude"]
        alt = gps["Altitude"]
        timestamp = gps["UTCTime"]

        if lat != "" and lon != "" and alt != "":
            pycom.rgbled(RGB_POS_FOUND)
            last_lat = lat
            last_lon = lon
            last_alt = alt
        else:
            pycom.rgbled(RGB_POS_NFOUND)

        data = {
            "device": "pytrack",
            "id": DevEUI,
            "lat": last_lat,
            "lon": last_lon,
            "alt": last_alt,
            "timestamp": timestamp,
            "battery": battery
        }

        # convert into JSON
        dataToSend = json.dumps(data)
        # Send the coordinates over LoRa
        s.send(dataToSend)

        print(dataToSend)

        time.sleep(1)

    except:
        pass
