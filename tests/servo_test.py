import RPi.GPIO as GPIO
from time import sleep

right_servo = 16
left_servo = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(right_servo, GPIO.OUT)
GPIO.setup(left_servo, GPIO.OUT)

pwm_right = GPIO.PWM(right_servo, 50)
pwm_left =GPIO.PWM(left_servo, 50)
pwm_right.start(0)
pwm_left.start(0)

pwm_right.ChangeDutyCycle(5)
pwm_left.ChangeDutyCycle(10)
sleep(1)

pwm_right.ChangeDutyCycle(7)
pwm_left.ChangeDutyCycle(7)
sleep(1)

pwm_right.ChangeDutyCycle(10)
pwm_left.ChangeDutyCycle(5)
sleep(1)

pwm_right.ChangeDutyCycle(7)
pwm_left.ChangeDutyCycle(7)
sleep(1)

pwm_right.stop()
pwm_left.stop()
GPIO.cleanup()