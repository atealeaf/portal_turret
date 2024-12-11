import RPi.GPIO as GPIO
from playsound import playsound

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.OUT)

GPIO.output(17, False)

input_count = 0
button_press = False

while True:
    if button_press is False and GPIO.input(4) == GPIO.HIGH:
        GPIO.output(17, True)