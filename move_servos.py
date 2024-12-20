"""
Move the TowerPro 9g SG90 Servos using a Raspberry Pi 4 Model B.

The servos can either move backward or forward.
"""
# Import necessary libraries
import RPi.GPIO as GPIO
from time import sleep

# Define the pins of the servos
right_servo = 16
left_servo = 18
GPIO.setmode(GPIO.BCM)

def servo_forward(sleep_time: int=1):
    """
    Moves the left and right servos forward.

    Inputs:
        sleep_time: Aan integer representing the amount of time
        the turret waits before moving the servo back to its 
        original position from the forward position.
    """
    GPIO.setup(right_servo, GPIO.OUT)
    GPIO.setup(left_servo, GPIO.OUT)

    pwm_right = GPIO.PWM(right_servo, 50)
    pwm_left =GPIO.PWM(left_servo, 50)
    pwm_right.start(0)
    pwm_left.start(0)
    pwm_right.ChangeDutyCycle(5)
    pwm_left.ChangeDutyCycle(9)
    sleep(sleep_time)

    pwm_right.ChangeDutyCycle(7)
    pwm_left.ChangeDutyCycle(7)
    sleep(0.5)

    pwm_right.stop()
    pwm_left.stop()

def servo_backward(sleep_time: int=1):
    """
    Moves the left and right servos backward.

    Inputs:
        sleep_time: Aan integer representing the amount of time
        the turret waits before moving the servo back to its 
        original position from the backward position.
    """
    GPIO.setup(right_servo, GPIO.OUT)
    GPIO.setup(left_servo, GPIO.OUT)

    pwm_right = GPIO.PWM(right_servo, 50)
    pwm_left =GPIO.PWM(left_servo, 50)
    pwm_right.start(0)
    pwm_left.start(0)
    pwm_right.ChangeDutyCycle(9)
    pwm_left.ChangeDutyCycle(5)
    sleep(sleep_time)

    pwm_right.ChangeDutyCycle(7)
    pwm_left.ChangeDutyCycle(7)
    sleep(0.5)

    pwm_right.stop()
    pwm_left.stop()
