import RPi.GPIO as GPIO
from playsound import playsound
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

input_count = 0
button_press = False
path_sounds = "./sounds/"
path_music = "./music/"

while True:
    if button_press is False and GPIO.input(7) == GPIO.HIGH:
        button_press = True
        input_count += 1
        # print(input_count)
        if input_count == 1:
            # Turret_turret_active_1-7.wav
            num = str(random.randint(1,7))
            playsound(path_sounds + "Turret_turret_active_" + num + ".wav")
        elif input_count == 2:
            # Turret_turret_autosearch_1-5.wav
            num = str(random.randint(1,5))
            playsound(path_sounds + "Turret_turret_autosearch_" + num + ".wav")
        elif input_count == 3:
            # Turret_turret_deploy_1-6.wav
            num = str(random.randint(1,6))
            playsound(path_sounds + "Turret_turret_deploy_" + num + ".wav")
        elif input_count == 4:
            # Turret_turret_pickup_1-7.wav
            num = str(random.randint(1,7))
            playsound(path_sounds + "Turret_turret_pickup_" + num + ".wav")
        elif input_count == 5:
            # Turret_turret_retire_1-7.wav
            num = str(random.randint(1,5))
            playsound(path_sounds + "Turret_turret_retire_" + num + ".wav")
        elif input_count == 6:
            # Turret_turret_search_1-3.wav
            num = str(random.randint(1,3))
            playsound(path_sounds + "Turret_turret_search_" + num + ".wav")
        elif input_count == 7:
            # Turret_turret_tipped_1-4.wav
            num = str(random.randint(1,4))
            playsound(path_sounds + "Turret_turret_tipped_" + num + ".wav")
            input_count = 0
    elif button_press is True and GPIO.input(7) == GPIO.LOW:
        button_press = False
        continue
