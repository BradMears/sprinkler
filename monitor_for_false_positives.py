#!/usr/bin/env python3
'''Watches the compressor sensor and prints out when the signal
goes high. Leave the compressor off during this so we can look
for false positives.'''

# Requires a sensor on pin 21 that will go high when the compressor 
# is running and low when it turns off.

import time
import datetime
import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
 
SENSOR_PIN = 21  # bottom right, GND is to the left

GPIO.setmode(GPIO.BCM)  # Set GPIO pins to BCM GPIO numbering
GPIO.setup(SENSOR_PIN, GPIO.IN)  # Set our input pin to be an input

trigger_time = 0

def handler(Pin):
    global trigger_time
    trigger_time = time.time()

GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=handler, bouncetime=200) 
print('Started monitoring at', datetime.datetime.now())
while True:
    # We use both interrupts and polling so we can keep printing
    # messages if the signal stays high for a while.
    if trigger_time != 0 or GPIO.input(SENSOR_PIN) == 1:
        # This shouldn't happen so let's complain about it
        print(datetime.datetime.now())
        trigger_time = 0
    time.sleep(1)
