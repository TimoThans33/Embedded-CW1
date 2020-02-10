
import time


import smbus
from collections import deque

# Create an instance
bus = smbus.SMBus(1)

# Register and config values of ADS1115
TempAddr = 0x48
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

# Accelerometer

AccAddr = 0x1F
AccID = 0xC7
RegStatus = 0x00
RegCtrlReg1 = 0x2A
RegCtrlReg2 = 0x2B
RegCtrlReg3 = 0x2C
RegXYZData = 0x0E
WhoAmI = 0x0D


# Log data the last maxlen seconds
Log = deque('',maxlen=60)
ValueStraight = 30550
ValueBend = 26600
ValuePerAngle = (ValueStraight-ValueBend)/90

def LogData(value):
    # Append the value in a list storing the last 60 values
    Log.appendleft(value)

def ValueToAngle(value):
    # Calculate the angle from the sensor
    return round(abs(value-ValueStraight)/ValuePerAngle,0)

def WriteI2C(Addr, Reg, Data):
    # Write data to reg
    bus.write_i2c_block_data(Addr, Reg, Data)

def ReadI2C(Addr, Reg, Len):
    # Read byte from reg
    return bus.read_i2c_block_data(Addr, Reg, Len)

def GetValueFromTempSensor():
    # Get the value of the sensor
    # data size 15 byte
    # Set OS
    data = OSConfig
    # Set Mux
    data |= ((0x04) & 0x07) << MuxOffset
    # Set Gain
    data |= Gain
    # Set Mode to single shot
    data |= ModeSingle
    # Set Data Rate
    data |= ConfigDR
    # Disable Comparator
    data |= CompDisable
    WriteI2C(TempAddr, Config, [(data >> 8) & 0xFF, data & 0xFF])
    # Wait for the data
    time.sleep(1/DataRate+0.0001)

    bytes = ReadI2C(TempAddr, Conversion, 2)

    return int.from_bytes(bytes, "big")


def SetModeAccSensor():
    id =  ReadI2C(AccAddr, WhoAmI, 1)
    print(id)
    print(int.from_bytes(id, "big"))



#def GetValueFromAccSensor():

SetModeAccSensor()    

while False:
    value = GetValueFromTempSensor()
    angle = ValueToAngle(value)
    LogData(angle)
    print(LogData)

    time.sleep(1)
