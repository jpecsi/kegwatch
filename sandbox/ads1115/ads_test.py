#####################################################################################
# Example program for the ADS1115_mPy module
#
# This program shows how to use the ADS1115 in single shot mode. 
#  
# Further information can be found on (currently only for the Arduino version):
# https://wolles-elektronikkiste.de/ads1115 (German)
# https://wolles-elektronikkiste.de/en/ads1115-a-d-converter-with-amplifier (English)
# 
#####################################################################################

from machine import I2C, Pin
from time import sleep
from ADS1115 import *

ADS1115_ADDRESS = 0x48

i2c = I2C(scl=Pin(22), sda=Pin(21))
adc = ADS1115(ADS1115_ADDRESS, i2c=i2c)
adc.setVoltageRange_mV(ADS1115_RANGE_6144)
adc.setCompareChannels(ADS1115_COMP_0_GND)
adc.setMeasureMode(ADS1115_SINGLE)


def readChannel(channel):
    adc.setCompareChannels(channel)
    adc.startSingleMeasurement()
    while adc.isBusy():
        pass
    voltage = adc.getResult_V()
    return voltage


def monitor_tap(t,n):
    close_tap = 1.85
    fully_open = 1.67
    if readChannel(t) >= fully_open and readChannel(t) < close_tap:
        print("Tap " + n + " Opening")
    if readChannel(t) < fully_open:
        print("Tap " + n + " Pouring Beer")
    if readChannel(t) >= close_tap:
        print("Tap " + n + " Closed")


while True:
    
    close_tap = 1.85
    fully_open = 1.67
    
    if readChannel(ADS1115_COMP_1_GND) >= fully_open:
        monitor_tap(ADS1115_COMP_1_GND, "1")
    if readChannel(ADS1115_COMP_2_GND) >= fully_open:
        monitor_tap(ADS1115_COMP_2_GND, "2")

        
    
    #print("TAP 1: " + str(readChannel(ADS1115_COMP_1_GND)) + " | TAP 2: " + str(readChannel(ADS1115_COMP_2_GND)))
    sleep(0.1)

