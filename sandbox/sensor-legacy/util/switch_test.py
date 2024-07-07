#!/usr/bin/env python3

# ========== LIBRARIES ========== #
import time, os
import RPi.GPIO as GPIO 
import configparser
from datetime import datetime

# Tap 1 Handler
def tap1(channel):
    # Setup Variables
    global t1_start
    global t1_end

    # If tap opens, start the timer...
    if GPIO.input(channel) == 1:  
        t1_start = time.perf_counter()      # Start the timer
        GPIO.output(t1_led,GPIO.HIGH)       # Turn on the tap's LED
        print("[TAP 1] Open")
      
    
    # If tap closes, stop the timer and report the amount of time tap was open
    if GPIO.input(channel) == 0:
        t1_end = time.perf_counter()        # Stop the timer
        GPIO.output(t1_led,GPIO.LOW)        # Turn off the tap's LED
        time_open = (t1_end - t1_start)     # Figure out how long tap was open
        print("[TAP 1] Closed After " + str(time_open) + " seconds")

        
    

# Tap 2 Handler
def tap2(channel):
    # Setup variables
    global t2_start
    global t2_end

    # If tap opens, start the timer...
    if GPIO.input(channel) == 1:
        t2_start = time.perf_counter()      # Start the timer
        GPIO.output(t2_led,GPIO.HIGH)       # Turn on the tap's LED
        print("[TAP 2] Open")
    
    # If tap closes, stop the timer and report the amount of time tap was open
    if GPIO.input(channel) == 0:
        t2_end = time.perf_counter()        # Stop the timer
        GPIO.output(t2_led,GPIO.LOW)        # Turn off the tap's LED
        time_open = (t2_end - t2_start)     # Figure out how long tap was open
        print("[TAP 2] Closed After " + str(time_open) + " seconds")






# ========== MAIN ========== #
if __name__ == '__main__':

    # ===== SET WORKING DIRECTORY ===== #
    cf_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config'))
    cf = cf_path + "/settings.conf"

    # ===== LOAD CONFIGURATION ===== #
    # Read config and beer files
    config = configparser.ConfigParser()
    config.read(cf)

    # Collection of taps
    taps = {
        1: "tap_1",
        2: "tap_2"
    }


    # ===== SETUP ===== #
    # Hardware Configuration
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # Tap 1
    t1_gpio = config.getint("tap_1","switch_gpio")              # Reed switch GPIO pin
    t1_led = config.getint("tap_1","led_gpio")                  # LED GPIO Pin
    GPIO.setup(t1_gpio,GPIO.IN)                                 # Configure the switch
    GPIO.setup(t1_led,GPIO.OUT)                                 # Configure the LED
    GPIO.add_event_detect(t1_gpio, GPIO.BOTH, callback=tap1,bouncetime=100)    # Handler to listen for switch

    # Tap 2
    t2_gpio = config.getint("tap_2","switch_gpio")              # Reed switch GPIO pin
    t2_led = config.getint("tap_2","led_gpio")                  # LED GPIO pin
    GPIO.setup(t2_gpio,GPIO.IN)                                 # Configure the switch
    GPIO.setup(t2_led,GPIO.OUT)                                 # Configure the LED
    GPIO.add_event_detect(t2_gpio, GPIO.BOTH, callback=tap2,bouncetime=100)    # Handler to listen for switch

    try:
        # Display starting status
        print("\n[KegWatch Switch Placement Test]\n================================")
        print("[SYSTEM] Ready!")

        if GPIO.input(t1_gpio) == 0:
            t1_stat = "CLOSED"
            GPIO.output(t1_led,GPIO.LOW)
        else:
            t1_stat = "OPEN"

        if GPIO.input(t2_gpio) == 0:
            t2_stat = "CLOSED"
            GPIO.output(t2_led,GPIO.LOW)
        else:
            t2_stat = "OPEN"

        print("[TAP 1] Current Status is " + t1_stat)
        print("[TAP 2] Current Status is " + t2_stat)
        persist = input()
    except KeyboardInterrupt:
        print("\n[" + str(datetime.now()) + "] EXITING")
        exit()
