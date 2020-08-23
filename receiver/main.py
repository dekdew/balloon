import pycom
from network import LoRa
import socket
import time
import json

# Colors used for status LED
RGB_OFF = 0x000000
RGB_POS_UPDATE = 0x101000
RGB_POS_FOUND = 0x001000
RGB_POS_NFOUND = 0x100000
RGB_LORA = 0x0000FF
LED_TIMEOUT = 0.2
pycom.heartbeat(False)

# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)


def getRecvData():
    data = ""
    msg = s.recv(10000)

    if not msg == b"":
        msg = msg.decode("utf-8")   # decode
        data = json.loads(msg)      # parse msg to json

        pycom.rgbled(RGB_POS_UPDATE)
        time.sleep(LED_TIMEOUT)
        pycom.rgbled(RGB_OFF)

    return data


geo_data = None
sensor_data = None

while True:
    try:
        data = getRecvData()

        if data == "":
            time.sleep(1)
            continue

        if data["device"] == 'pytrack':
            geo_data = data

        if data["device"] == 'sensor':
            sensor_data = data

        if geo_data and sensor_data:
            clean_data = geo_data
            clean_data["humidity"] = sensor_data["humidity"]
            clean_data["temp"] = sensor_data["temp"]
            clean_data["pressure"] = sensor_data["pressure"]

            # convert into JSON
            dataToSerial = json.dumps(clean_data)
            print(dataToSerial)

            pycom.rgbled(RGB_LORA)
            time.sleep(LED_TIMEOUT)
            pycom.rgbled(RGB_OFF)

            # reset data
            geo_data = None
            sensor_data = None

        time.sleep(1)

    except:
        pass
