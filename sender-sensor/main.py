import pycom
import time
import gc
import socket
from network import LoRa
import ubinascii
import json
from htu21d import HTU21D
from ms5611 import MS5611

#init sensor
ms = MS5611()
htu = HTU21D()

# delay time
delay = 1

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


while True:
    try:
        temp = (htu.temperature + ms.temperature) / 2
        pressure = ms.pressure
        humidity = htu.relative_humidity

        data = {
            "device": "sensor",
            "id": DevEUI,
            "temp": temp,
            "pressure": pressure,
            "humidity": humidity
        }

        # convert into JSON
        dataToSend = json.dumps(data)
        print(dataToSend)
        
        # Send the coordinates over LoRa
        s.send(dataToSend)

        # blink RGB to green
        pycom.rgbled(RGB_POS_FOUND)
        time.sleep(LED_TIMEOUT)
        pycom.rgbled(RGB_OFF)

        time.sleep(delay)

    except:
        # blink RGB to red
        pycom.rgbled(RGB_POS_NFOUND)
        time.sleep(LED_TIMEOUT)
        pycom.rgbled(RGB_OFF)
