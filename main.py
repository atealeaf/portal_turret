"""
This module runs the main loop for the Portal Turret replica using
an IR remote. The turret can run in many modes, including stimulus
detection, music playback with dancing, music playback without
dancing, and manual mode.
"""

import os
import sys
import time 
import threading
import RPi.GPIO as GPIO
import queue  # Import the queue module

# Important necessary functions and classes
from play_sounds import PlaySounds
from play_music import PlayMusic
from ir_receiver import initialize_ir, read_ir
from acceleration import sounds_acceleration
from move_wings import move_motors
from move_servos import servo_backward, servo_forward

# Initialize the IR remote control
client = initialize_ir()

# Set up timing controls
previous_time = time.time()
gyro_start_time = time.time()

# Other starting variables we need
mode = -1
# Time in seconds to wait before allowing another press
debounce_time = 0.5  
last_signal = None

# Initialize the sound player
current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

sound_directory = current_directory + "/sounds"
sound_player = PlaySounds(sound_directory)

# Initialize the music player
music_directory = current_directory + "/music"
music_player = PlayMusic(music_directory)

# Create a queue to hold IR signals
signal_queue = queue.Queue()

# Function to handle IR signals
def handle_ir_signals():
    """
    Read the current IR signal. Depending on the signal, 
    different actions may occur.
    """
    global mode, previous_time
    while True:
        signal = read_ir(client)

        # Calculate the current time and time elapsed
        current_time = time.time()
        time_elapsed = current_time - previous_time

        # If the power button is pressed, turn off the robot
        if signal == "KEY_POWER":
            sound_player.play_sound("retire", True)
            print("Turning off...")
            break
        
        # If "Mode" is pressed, cycle through the modes
        if signal == "KEY_MODE" and time_elapsed > debounce_time:
            mode += 1  # Increment the mode
            print(f"Mode: {mode % mode_count} ({modes[mode % mode_count]})")
            # Update the previous_time to the current time
            previous_time = current_time  

        # Put the signal in the queue
        signal_queue.put(signal)

# Start the IR signal handling in a separate thread
ir_thread = threading.Thread(target=handle_ir_signals)
ir_thread.daemon = True 
ir_thread.start()

# Start loop
try:
    # Define the different modes
    modes = [
        "stimulus_detection", 
        "music_dance", 
        "music_no_dance", 
        "manual"]
    mode_count = len(modes)  # This will help us wrap around later

    # Start up sound
    sound_player.play_sound("deploy", False)
    move_motors(move_in=False)
    servo_forward(sleep_time=2)
    move_motors(move_out=False)

    # Loop to run through the modes
    while True:
        # Check for signals in the queue
        while not signal_queue.empty():
            signal = signal_queue.get()
            # Handle the signal as needed
            if signal == "KEY_POWER":
                break  # Exit the loop if power is pressed
            # You can add more signal handling logic here if needed

        # Mode 0 - Stimulus Detection
        if mode % mode_count == 0:
            sounds_acceleration(sound_player, gyro_start_time)
            time.sleep(0.5)  # Adjust the sleep time as needed

        # Mode 1 - Play Music and Dance!
        elif mode % mode_count == 1:
            while True:
                if music_player.ir_play(client, True):
                    break
                else:
                    music_player.ir_play(client, True)
            time.sleep(0.5) 

        # Mode 2 - Play Music and No Dancing
        elif mode % mode_count == 2:
            print("music no dance")
            while True:
                if music_player.ir_play(client, dance=False):
                    break
                else:
                    music_player.ir_play(client, dance=False)
            time.sleep(0.5)

        # Mode 3 - Manual
        elif mode % mode_count == 3:

            sound_dictionary = {
                "1": "active",
                "2": "autosearch",
                "3": "deploy",
                "4": "pickup",
                "5": "retire",
                "6": "search",
                "7": "tipped"
            }

            while not signal_queue.empty():
                signal = signal_queue.get()
                new_signal = False
            
                # TODO: Fix this logic!

                if signal != last_signal:
                    # Update the last processed signal
                    print(f"Received signal: {signal}")
                    last_signal = signal 
                    new_signal = True

                if new_signal:
                    if last_signal in sound_dictionary:
                        sound_player.play_sound(sound_dictionary[signal], True)

                    elif last_signal == "8":
                        print("Motors moving")
                        move_motors(speed=75)

                    elif last_signal == "9":
                        print("Servos moving")
                        servo_forward()

                time.sleep(0.1)
        
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.close()
    GPIO.cleanup()
