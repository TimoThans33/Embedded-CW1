
import time
import os
import math
import smbus
import struct
import paho.mqtt.client as mqtt
from collections import deque
from urllib.parse import urlparse

# Create an instance
bus = smbus.SMBus(1)

# MQTT

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set("tvbxqfql", "bTziEuFTZSZb")
client.connect("broker.mqttdashboard.com")
client.loop_start()

mqttc.publish(topic, 2)
mqttc.subscribe(topic, 0)


rc = 0
while rc == 0:
    rc = mqttc.loop()
print("rc: " + str(rc))

Timer = time.time()

# Register and config values of ADS1115
FlexAddr = 0x48
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

# Register and config values of FXOS8700

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
LogFlex = deque('',maxlen=60)
LogPitch = deque('',maxlen=60)
LogRoll = deque('',maxlen=60)

ValueStraight = 30550
ValueBend = 26600
ValuePerAngle = (ValueStraight-ValueBend)/90

MagMcro = 0.000001
AccMG2G = 0.000244
Gravity = 9.82
pitch = 0.0
roll = 0.0
dt = 0.01

def LogData(value, log):
    # Append the value in a list storing the last 60 values
    log.appendleft(value)

def ValueToAngle(value):
    # Calculate the angle from the sensor
    return round(abs(value-ValueStraight)/ValuePerAngle,0)

def WriteI2C(Addr, Reg, Data):
    # Write data to reg
    bus.write_i2c_block_data(Addr, Reg, Data)

def ReadI2C(Addr, Reg, Len):
    # Read byte from reg
    return bus.read_i2c_block_data(Addr, Reg, Len)

def GetValueFromFlexSensor():
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
    WriteI2C(FlexAddr, Config, [(data >> 8) & 0xFF, data & 0xFF])
    # Wait for the data
    time.sleep(1/DataRate+0.0001)

    bytes = ReadI2C(FlexAddr, Conversion, 2)

    return int.from_bytes(bytes, "big")


def SetModeAccSensor():
    if  int.from_bytes(ReadI2C(AccAddr, WhoAmI, 1), "big") != AccID:
        print("Failed to find Accelerometer")
        exit()
    # Enable changes in control register
    bus.write_byte_data(AccAddr, CtrlReg1, 0x00)
    # 2g Full-scale range
    bus.write_byte_data(AccAddr, XYZData, 0x00)
    # High Resolution
    bus.write_byte_data(AccAddr, CtrlReg2, 0x02)
    # 50Hz, ODR 100hZ, Redused Noise, Normal, Active
    bus.write_byte_data(AccAddr, CtrlReg1, 0x15)     # 00010101
    # Auto Dis, No Mag, No Action, hybrid
    bus.write_byte_data(AccAddr, MCtrlReg1, 0x1F)    # 00011111


def GetValueFromAccGyroSensor():
    # Read Accelerometer Sensor
    buffer = ReadAccGyrobyte(OutMSB, 6)
    Acc = FormatData(buffer, True)
    # Read Gyrometer Sensor
    buffer = ReadAccGyrobyte(MOutMSB, 6)
    Gyro = FormatData(buffer)

    return ([x*AccMG2G for x in Acc]),([y*MagMcro for y in Gyro])


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


while False:
    Acc, Gyro = GetValueFromAccGyroSensor()
    pitch += Gyro[0]*dt
    roll -= Gyro[1]*dt

    pitchAcc = math.atan2(Acc[1], Acc[2])*180/math.pi
    pitch = pitch*0.98 + pitchAcc*0.02

    rollAcc = math.atan2(Acc[0], Acc[2])*180/math.pi
    roll = roll*0.98 + rollAcc*0.02

    time.sleep(dt)

    if (time.time() - Timer) >= 1:
        # Every Ssecond

        value = GetValueFromFlexSensor()
        angle = ValueToAngle(value)
        # Store Data
        LogData(angle, LogFlex)
        LogData(pitch, LogPitch)
        LogData(roll, LogRoll)
        print(angle, pitch, roll)
        Timer = time.time()
        client.publish('neck', angle)
        client.publish('back', roll)
        #client.publish('time', time.time())
