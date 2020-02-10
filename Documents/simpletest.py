
import time


#import smbus
from collections import deque

# Create an instance
#bus = smbus.SMBus(1)

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

channel = 0
config = OSConfig
print(hex(config))
print(((channel+0x04) & 0x07) << MuxOffset)
config |= ((channel+0x04) & 0x07) << MuxOffset
print(hex(config))
config |= ModeSingle
print(hex(config))
config |= ConfigDR
print(hex(config))
print(config)
print([(config >> 8) & 0xFF,config & 0xFF])





while False:


    print(value)
    angle = ValueToAngle(value)
    LogData(angle)
    print(angle)

    time.sleep(1)
