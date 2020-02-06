# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15
from collections import deque

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Log data the last maxlen seconds
Log = deque('',maxlen=60)
ResistanceStraight = 37300
ResistanceBend = 90000
VDD = 5
RDiv = 47000


def LogData(value):
    # Append the value in a list storing the last 60 values
    Log.appendleft(value)

def ValueToAngle(value):
    # Calculate the angle from the sensor
    flexV = value*VDD/1023
    print(flexV)
    flexR = RDiv*(VDD/flexV-1)
   # angle = map(flexR, ResistanceStraight, ResistanceBend, 0, 90)
   # return Angle
    print(flexR)


# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(1)))
print('-' * 37)
# Main loop.



while True:
    # Read all the ADC channel values in a list.
    value = adc.read_adc(1, gain=GAIN, data_rate=128)
    # print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*value))
    # Pause for a second
    print(value)
    angle = ValueToAngle(value)
  #  LogData(angle)
   # print(angle)#

    time.sleep(1)
