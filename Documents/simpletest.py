
import time

import math
import smbus
import struct
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
CtrlReg1 = 0x2A
CtrlReg2 = 0x2B
XYZData = 0x0E
WhoAmI = 0x0D
OutMSB = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
MCtrlReg1 = 0x5B
MCtrlReg2 = 0x5C
MOutMSB = [0x33, 0x34, 0x35, 0x36, 0x37, 0x38]

# Log data the last maxlen seconds
Log = deque('',maxlen=60)

ValueStraight = 30550
ValueBend = 26600
ValuePerAngle = (ValueStraight-ValueBend)/90

MagMcro = 0.1
AccMG2G = 0.000244
AccMG4G = 0.000488
Gravity = 9.82
GyroAngle = [0.0]*3
AccAngle = [0.0]*2
Angle = [0.0]*2

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
    if  int.from_bytes(ReadI2C(AccAddr, WhoAmI, 1), "big") != AccID:
        print("Failed to find Accelerometer")
        exit()
    bus.write_byte_data(AccAddr, CtrlReg1, 0x00)
    bus.write_byte_data(AccAddr, XYZData, 0x00)
    bus.write_byte_data(AccAddr, CtrlReg2, 0x02)
    bus.write_byte_data(AccAddr, CtrlReg1, 0x15) # 00100101
    bus.write_byte_data(AccAddr, MCtrlReg1, 0x1F)    # 00011111


def GetValueFromAccGyroSensor():
    buffer = ReadAccGyrobyte(OutMSB, 6)
    Acc = FormatData(buffer, True)
    buffer = ReadAccGyrobyte(MOutMSB, 6)
    Gyro = FormatData(buffer)


    return ([x*AccMG4G for x in Acc]),([y*MagMcro for y in Gyro])


def FormatData(buffer, convert=None):
    data = [0]*3
    for i in range(3):
        byte = struct.unpack_from('>H', buffer[i*2:i*2+2])[0]
        if convert == True:
            data[i] = TwosComp(byte >> 2, 14)
        else:
            data[i] = byte
    return data

def ReadAccGyrobyte(reg, length):
    buffer = bytearray(length)
    k = 0
    for i in reg:
        buffer[k] =  bus.read_byte_data(AccAddr, i)
        k += 1
    return buffer

def TwosComp(val, bits):
    if val & (1 << (bits - 1)) != 0:
        return val - (1 << bits)
    return val

SetModeAccSensor()


while True:
    Acc, Gyro = GetValueFromAccGyroSensor()
    AccAngle[0] = math.atan2(Acc[1],Acc[2]+math.pi)*180/math.pi
    AccAngle[1] = math.atan2(Acc[2],Acc[0]+math.pi)*180/math.pi
    Angle[0] = 0.98*(Angle[0]+Gyro[0]*0.2) + (1-0.92)*AccAngle[0]
    Angle[1] = 0.98*(Angle[1]+Gyro[1]*0.2) + (1-0.92)*AccAngle[1]
    print(AccAngle)
    print(Angle)
    time.sleep(0.5)

while False:
    value = GetValueFromTempSensor()
    angle = ValueToAngle(value)
    LogData(angle)
    print(LogData)

    time.sleep(1)
