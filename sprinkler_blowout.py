#!/usr/bin/env python3
'''Automates blowing out our household sprinkler system.'''

# Requires a sensor on pin 21 that will go high when the compressor 
# is running and low when it turns off.
# Requires network access to the OpenSprinklerPi that controls the
# relays that open and close the valves.

import time
import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
from control_ospi import set_zone, NUM_ZONES

SENSOR_PIN = 21  # bottom right, GND is to the left

GPIO.setmode(GPIO.BCM)  # Set GPIO pins to BCM GPIO numbering
GPIO.setup(SENSOR_PIN, GPIO.IN)  # Set our input pin to be an input

trigger_time = 0
state = "ON" if GPIO.input(SENSOR_PIN) else "OFF"

def handler(Pin):
    global trigger_time
    global state
    trigger_time = time.time()
    state = 'ON'

# The bounce time of 200 ms was arrived at empirically i.e. I tried different
# values and 200 seemed to work well with no false positives.
GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=handler, bouncetime=200) 
'''
while True:
    time_since_trigger = time.time() - trigger_time
    if GPIO.input(SENSOR_PIN) == 0 and time_since_trigger >= 2:
        state = 'OFF'
    msg = f"Compressor: {state}"
    print(msg)
    time.sleep(1)
'''

def shut_it_all_down_and_quit():
    '''Something went wrong so let's try to shut off all the zones
    and terminate.'''
    for zone in range(1,NUM_ZONES+1):
        print('Closing zone', zone)
        set_zone(zone, 0)
        time.sleep(1)

def blowout_zone(zone, duration):
    '''Applies pressure to the line for the specified number of seconds.
    Stops counting time while the compressor refills.'''
    rc = set_zone(zone, 1)
    if rc : 
        shut_it_all_down_and_quit()

    while duration > 0:
        #time_since_trigger = time.time() - trigger_time

        global trigger_time
        global SENSOR_PIN
        if trigger_time != 0 or GPIO.input(SENSOR_PIN) == 1:
            # The compressor has turned on. Wait for it to refill
            print('Closing valve while compressor fills')
            # Turn the zone off
            rc = set_zone(zone, 0)
            if rc : 
                shut_it_all_down_and_quit()
            while GPIO.input(SENSOR_PIN):
                time.sleep(1)
            trigger_time = 0
            # Turn it back on
            print('Compressor ready. Opening valve again.')
            rc = set_zone(zone, 1)
            if rc : 
                shut_it_all_down_and_quit()

        duration -= 1
        time.sleep(1)

    # Turn it off
    print(f'Turning off zone {zone}')
    rc = set_zone(zone, 0)
    if rc : 
        shut_it_all_down_and_quit()

for zone in range(1,NUM_ZONES+1):
    print(f'Blowing out zone {zone}')
    blowout_zone(zone, 120)

print('Complete')
