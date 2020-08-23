# Balloon

# Usage

 1. Plug the Receiver to computer
 2. Clone this repo then config receiver connected port and database in [read-serial/main.py](https://github.com/dekdew/balloon/blob/master/read-serial/main.py "main.py")
```python
SERIAL_DEVICE  =  'YOUR-PORT'  # change to receiver connected port
```
```python
USER = 'YOUR-DB-USER'
PASSWORD = 'YOUR-DB-PASSWORD'
HOST = 'YOUR-DB-HOST'
PORT = 'YOUR-DB-PORT'
DATABASE = 'YOUR-DB-DATABASE'
```
 3. Run [read-serial/main.py](https://github.com/dekdew/balloon/blob/master/read-serial/main.py "main.py")
```python
# MacOS
python3 main.py

# Windows
py -3 main.py
```

## [Read Serial from Receiver](https://github.com/dekdew/balloon/tree/master/read-serial)

# Hardware

## [Sender (GPS)](https://github.com/dekdew/balloon/tree/master/sender-gps)
![enter image description here](https://raw.githubusercontent.com/dekdew/balloon/master/assets/sernder-gps.png)

## [Sender (Sensor)](https://github.com/dekdew/balloon/tree/master/sender-sensor)
![enter image description here](https://raw.githubusercontent.com/dekdew/balloon/master/assets/sernder-sensor.png)

## [Receiver](https://github.com/dekdew/balloon/tree/master/receiver)
