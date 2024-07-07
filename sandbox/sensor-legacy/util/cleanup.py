#!/usr/bin/env python3

import os
import configparser
import RPi.GPIO as GPIO

if __name__ == '__main__':

    # Set working directory
    cf_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config'))
    cf = cf_path + "/settings.conf"

    # Read config and beer files
    config = configparser.ConfigParser()
    config.read(cf)

    # Hardware Configuration
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # Tap 1
    t1_gpio = config.getint("tap_1","switch_gpio")                              # Reed switch GPIO pin
    t1_led = config.getint("tap_1","led_gpio")                                  # LED GPIO Pin
    GPIO.setup(t1_gpio,GPIO.IN)                                                 # Configure the switch
    GPIO.setup(t1_led,GPIO.OUT)                                                 # Configure the LED

    # Tap 2
    t2_gpio = config.getint("tap_2","switch_gpio")                              # Reed switch GPIO pin
    t2_led = config.getint("tap_2","led_gpio")                                  # LED GPIO pin
    GPIO.setup(t2_gpio,GPIO.IN)                                                 # Configure the switch
    GPIO.setup(t2_led,GPIO.OUT)  

    GPIO.cleanup()
