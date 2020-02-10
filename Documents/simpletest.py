
import time


import smbus
from collections import deque

# Create an instance
bus = smbus.SMBus(1)

# Register and config values of ADS1115
Addr = 0x48
Conversion = 0x00
Config = 0x01
LowThreshold = 0x02
HighThreshold = 0x03
ModeSingle = 0x0100
ModeContinuous = 0x0000
OSConfig = 0x8000
ConfigDR = 0x0040
MuxOffset = 12
Gain = 0x0200
CompDisable = 0x0003
DataRate = 32

# Log data the last maxlen seconds
Log = deque('',maxlen=60)
ValueStraight = 31800
ValueBend = 27000
ValuePerAngle = (ValueStraight-ValueBend)/90

def LogData(value):
    # Append the value in a list storing the last 60 values
    Log.appendleft(value)

def ValueToAngle(value):
    # Calculate the angle from the sensor
    return round(abs(value-ValueStraight)/ValuePerAngle,0)

def WriteI2C(Reg, Data):
    # Write data to reg
    bus.write_i2c_block_data(Addr, Reg, Data)

def ReadI2C(Reg, Len):
    # Read byte from reg
    return bus.read_i2c_block_data(Addr, Reg, Len)

def GetValueFromSensor(channel):
    # Get the value of the sensor
    reg = OSConfig
    reg |= ((channel+0x04) & 0x07) << MuxOffset
    reg |= Gain
    reg |= ModeSingle
    reg |= ConfigDR
    reg |= CompDisable
    WriteI2C(Config, [(reg >> 8) & 0xFF, reg & 0xFF])
    # Wait for the data
    time.sleep(1/DataRate+0.0001)

    bytes = ReadI2C(Conversion, 2)

    return int.from_bytes(bytes, "big")





while True:
    value = GetValueFromSensor(0)
    print(value)
    angle = ValueToAngle(value)
    LogData(angle)
    print(angle)

    time.sleep(1)
