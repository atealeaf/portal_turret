import os
import sys
from play_sounds import PlaySounds
from move_wings import move_motors
from play_music import PlayMusic
from acceleration import get_acceleration
import time 
from ir_receiver import initialize_ir, read_ir
import lirc
from move_servos import servo_backward, servo_forward

move_motors(move_out=False)

move_motors(move_out=True, move_in=False)
time.sleep(0.5)
servo_forward(sleep_time=2)
time.sleep(0.5)
move_motors(move_out=False, move_in=True)



"""
# client = initialize_ir()

# print(type(client))
# Define the music directory
music_directory = os.path.dirname(os.path.abspath(sys.argv[0])) + "/sounds"
music_player = PlaySounds(music_directory)

try:
    music_player.play_on_press()
except KeyboardInterrupt:
    # client.close()
    print("end")

# client = initialize_ir()

# key_map = {
#     "KEY_MODE": "mode",
#     "KEY_PLAYPAUSE": "playpause",
#     "KEY_NEXTSONG": "next",
#     "KEY_PREVIOUSSONG": "back"
# }

# try:
#     while True:
#         music_player.ir_play(client)

# except KeyboardInterrupt:
#     client.close()


# Define the sound directory
sound_directory = os.path.dirname(os.path.abspath(sys.argv[0])) + "/sounds"
sound_player = PlaySounds(sound_directory)

picked_up = False
start_time = time.time() - 5

while True:

    current_time = time.time()
    elapsed_time = current_time - start_time

    acceleration = get_acceleration(False)
    vertical = acceleration[2]

    if vertical < 9 and elapsed_time > 5:
        sound_player.play_sound("pickup", True)
        start_time = time.time()

    time.sleep(0.5)
"""