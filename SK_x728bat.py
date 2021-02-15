# Signal K Plugin for Suptronics x728 UPS RPi Hat
# by Chuck Bowers - Rhumb Runner J/29 - San Diego, CA
#
# Revsion 0.0.1
#
# Module reads the Voltage and capacity over I2C and
# sends the data to SK every 2 seconds.
# It also monitors GPIO 6 which is the GPIO for
# PLD (Power Loss Dectection) when the PLD jumper is
# in place. It sends an update to SK upon detection
# to raise an alarm.
#
import struct
import smbus
import sys
import time
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)

skData1 = ''
SkData2 = ''

def readVoltage(bus):

     address = 0x36
     read = bus.read_word_data(address, 2)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     voltage = swapped * 1.25 /1000/16
     return voltage


def readCapacity(bus):

     address = 0x36
     read = bus.read_word_data(address, 4)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     capacity = swapped/256
     return capacity

bus = smbus.SMBus(1) # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

def my_callback(channel):
    if GPIO.input(6):     # if port 6 == 1
        # print("---AC Power Loss OR Power Adapter Failure---")
        skData1 = '{"updates": [{ "values": [{"path": "enviroment.rpi.ups.active","value": true }]}]}'
        serial_dict = json.loads(skData1.encode('ascii', 'strict'))
        sys.stdout.write(json.dumps(serial_dict))
        sys.stdout.write('\n')
        sys.stdout.flush()
    else:                  # if port 6 != 1
        # print("---AC Power OK,Power Adapter OK---")
        skData1 = '{"updates": [{ "values": [{"path": "enviroment.rpi.ups.active","value": false }]}]}'
        serial_dict = json.loads(skData1.encode('ascii', 'strict'))
        sys.stdout.write(json.dumps(serial_dict))
        sys.stdout.write('\n')
        sys.stdout.flush()

GPIO.add_event_detect(6, GPIO.BOTH, callback=my_callback)

while True:

 # print("******************")
 # print("Voltage:%5.2fV" % readVoltage(bus))
 # print("Battery:%5i%%" % readCapacity(bus))
 UPSCapacity= readCapacity(bus)

 if UPSCapacity >= 100:
    UPSCapacity = 100

 if readCapacity(bus) < 20:
    # print("Battery LOW")
 # print("******************")

 skData1 = '{"updates": [{ "values": [{"path": "enviroment.rpi.ups.voltage","value": "' + str(readVoltage(bus)) +'"}]}]}'
 skData2 = '{"updates": [{ "values": [{"path": "enviroment.rpi.ups.capacity","value": "' + str(UPSCapacity) + '"}]}]}'
 serial_dict = json.loads(skData1.encode('ascii', 'strict'))
 sys.stdout.write(json.dumps(serial_dict))
 sys.stdout.write('\n')
 serial_dict = json.loads(skData2.encode('ascii', 'strict'))
 sys.stdout.write(json.dumps(serial_dict))
 sys.stdout.write('\n')
 sys.stdout.flush()

 time.sleep(2)