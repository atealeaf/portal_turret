"""
A Python program to read acceleration and magnetism on a gyroscope on a
Raspberry Pi Model B. Specifically, this reads the SM303AGR gyroscope.

Includes a function to play sounds depending on the acceleration values
read.
"""

# Import libraries
import board
import busio
import adafruit_lis2mdl
import adafruit_lsm303_accel
import time
from time import sleep

def get_acceleration(debug: bool=False):
    """
    Gets the acceleration and magnetism read by the gyroscope.

    Inputs:
        debug: A boolean that determines whether the acceleration
        and magnetism values are printed to the terminal.

    Returns:
        accel.acceleration: A tuple representing the acceleration
        values for three axes. The values in the tuples are floats.
    """

    i2c = busio.I2C(board.SCL, board.SDA)
    mag = adafruit_lis2mdl.LIS2MDL(i2c)
    accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

    if debug:
        while True:
            print("Acceleration (m/s^2): X=%0.3f Y=%0.3f",
                  "Z=%0.3f"%accel.acceleration)
            print("Magnetometer (micro-Teslas)): X=%0.3f",
                 "Y=%0.3f Z=%0.3f"%mag.magnetic)
            print("")
    else:
        return accel.acceleration
    
def sounds_acceleration(sound_player, gyro_start_time, cooldown=3):
    """
    Determines if the acceleration is below a certain threshold (in
    this case, whether the gyroscope is picked up) and play a sound
    if it is not on cooldown.

    Inputs:
        sound_player: A class object PlaySounds. This allows for audio
        to be played.
        gyro_start_time: A float representing the start time of the
        program.
    """
    # Time variables for cooldown
    gyro_current_time = time.time()
    gyro_elapsed_time = gyro_current_time - gyro_start_time

    # Specifically get the vertical acceleration
    acceleration = get_acceleration(False)
    vertical = acceleration[2]

    # If the conditions are met, play a sound and restart the cooldown
    if vertical < 9 and gyro_elapsed_time > cooldown:
        sound_player.play_sound("pickup", True)
        gyro_start_time = time.time()