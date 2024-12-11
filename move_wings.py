"""
A Python program to make motors move on a Raspberry Pi Model B.

This creates a function that moves motors using a L293D motor chip and
a DC motor. The motor is powered via an external battery.
"""

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

def move_motors(speed: int=50, time: float=0.75, Motor1A: 
               int=24, Motor1B: int=23, Motor1E: int=25,
               move_out: bool=True, move_in: bool=True):
    """
    Allows for the wings to move.

    Uses a motor to move the wings in and out.

    Inputs:
        Motor1A: An integer representing the pin associated with
        pin A on the L293D. This tells the motor to spin in one 
        direction.
        Motor1B: An integer representing the pin associated with
        pin B on the L293D. This tells the motor to spin in the
        opposite direction.
        Motor1E: An integer representing the pin associated with
        enable on the L293D. This turns on the motor
        move_out: A boolean representing whether to move the wings out.
        move_in: A boolean representing wheter to move the wings in.
    """

    # Initialize up the motors
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)

    # print("Start the motor")
    GPIO.output(Motor1E,GPIO.HIGH) # Turn on the motor

    # Control the motor speed with PWM
    pwm=GPIO.PWM(Motor1E,100)
    pwm.start(speed)

    # Make the motor move forward for some specified time
    # print("forward")
    if move_out:
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        sleep(time)

    # Make the motor move backward for some specified time
    # print("backward")
    if move_in:
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        sleep(time)

    GPIO.output(Motor1E,GPIO.LOW) # Turn off the motor
    pwm.stop()