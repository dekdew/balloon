import serial
import psycopg2
from datetime import datetime
import json

# set device port and baudrate
SERIAL_DEVICE = 'YOUR-PORT'  # change to receiver connected port
BAUDRATE = 115200

# DB config
USER = 'YOUR-DB-USER'
PASSWORD = 'YOUR-DB-PASSWORD'
HOST = 'YOUR-DB-HOST'
PORT = 'YOUR-DB-PORT'
DATABASE = 'YOUR-DB-DATABASE'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# set table
TABLE = 'geo'

try:
    connection = psycopg2.connect(user=USER,
                                  password=PASSWORD,
                                  host=HOST,
                                  port=PORT,
                                  database=DATABASE)

    cursor = connection.cursor()
    print("Connected to PostgreSQL")
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

# init serial
ser = serial.Serial(SERIAL_DEVICE, BAUDRATE)

while True:
    try:
        # read serial
        msg = ser.readline()
        msg = msg.decode("utf-8")
        data = json.loads(msg)
        print("\ndata: ", data, "\n-------------------------------------------------------------")

        # current date and time
        timestamp = data["timestamp"]

        postgres_insert_query = """ INSERT INTO {} (device_id, lat, long, battery, timestamp, temp, pressure, humidity, altitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format(
            TABLE)
        record_to_insert = (data["id"], data["lat"], data["lon"],
                            data["battery"], timestamp, data["temp"], data["pressure"], data["humidity"], data["alt"],)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print("{}{} Record inserted successfully into {} table{}".format(bcolors.OKGREEN, count, TABLE, bcolors.ENDC))
    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("{}Failed to insert record into {} table{}".format(bcolors.FAIL, TABLE, bcolors.ENDC), error)
