"""
A Python program to detect sound using a Raspberry Pi 4 Model B.

To detect sound, a PCF8591 ADC/DAC and a Sunfounder Sound Sensor are
used.
"""

import adafruit_pcf8591.pcf8591 as ADC
import board
import busio
import RPi.GPIO as GPIO
import time
from move_wings import move_motors # Import motor movement functions

# Set the mode to BCM
GPIO.setmode(GPIO.BCM)

i2c = busio.I2C(board.SCL, board.SDA)
global adc # Create ADC object
adc = ADC.PCF8591(i2c)

def sense_sound(loop: bool=False):
    """
    Set up the sound sensing module (sound sensor and ADC).

    Inputs:
        loop: A boolean representing whether or not to run a loop with
        read_sound(). This is mainly used for debugging and testing 
        sound detection.
    """
    i2c = busio.I2C(board.SCL, board.SDA)
    global adc # Create ADC object
    adc = ADC.PCF8591(i2c)

    if loop:
        while True:
            read_sound()

def read_sound(threshold: int=115, dance: bool=True, debug: bool=False):
    """
    Reads the sound values from the sensor. Depending on the flags
    used, different actions will be performed.

    Inputs:
        threshold: An integer representing the cutoff threshold for
        determining whether or not a sound was detected.
        dance: A boolean representing whether or not to move the motors
        depending on the sound reading.
        debug: A boolean representing whether or not to enable print 
        statements for debugging.
    """
    # Read the analog input
    sound_value = adc.read(3)

    # If there is a sound value, perform these actions
    if sound_value is not None:
        if debug:
            print("Value:", sound_value)
        if sound_value < threshold:
            if debug:
                print("Voice In!!")
            if dance:
                move_motors(speed=75,time=0.5)
        time.sleep(0.1)