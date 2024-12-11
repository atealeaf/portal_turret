import RPi.GPIO as GPIO
from time import sleep

# Pins for Motor Driver Inputs 
Motor1A = 24
Motor1B = 23
Motor1E = 25
GPIO.setmode(GPIO.BCM)

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

pwm=GPIO.PWM(Motor1E,100) # configuring Enable pin means GPIO-04 for PWM 
pwm.start(25) # starting it with 50% dutycycle

print("Motor going to Start")

GPIO.output(Motor1A,GPIO.HIGH)
GPIO.output(Motor1B,GPIO.LOW)
GPIO.output(Motor1E,GPIO.HIGH)

sleep(1)

GPIO.output(Motor1A,GPIO.LOW)
GPIO.output(Motor1B,GPIO.HIGH)
GPIO.output(Motor1E,GPIO.HIGH)

sleep(1)

print("Stopping motor")

GPIO.output(Motor1E,GPIO.LOW) # to stop the motor

GPIO.cleanup()