"""
A Python program to play sounds on the Rapsberry Pi 4 Model B.

This creates a class to store sound files and folders and play them 
when commanded. It also allows for movement alongside the sounds
played.
"""

import random
import os
import sys
import glob
import RPi.GPIO as GPIO
from playsound import playsound
from move_wings import move_motors # Import motor movement functions

# Initiate the board for input
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class PlaySounds:
    """
    Create a class to play sounds on a Raspberry Pi 4 with Mu Code.

    When Mu Code is installed, it automatically creates some folders.
    Of those folders, we are interested in `music` and `sounds`.
    For this program to work, sound files must be put in `sounds` and
    categorized by sound file type (e.g. sound files for explosions and
    laughter must be put into different subfolders within the `sounds`
    folder).
    """

    def __init__(self, sound_directory: str):
        """
        Initialize variables to store within the class.

        This includes all of the sound files stored on the Raspberry Pi via
        Mu and the sound folders found within `mu_code/`.

        Inputs:
            sound_directory: A string representing the path to the
            folder containing the sound files (or folders).
        """

        # Paths to all sound files
        self.sound_files = glob.glob(os.path.join(sound_directory, '**', '*.wav'), recursive=True)
        # Get names of folders in sound directory
        self.sound_folders = self.directory_folders(sound_directory)

        # List all the available sound folers
        # print(f"Sound folders found: {list(self.sound_folders.keys())}")

    def directory_folders(self, sound_directory: str, file_type: str="*.wav"):
        """
        Create a dictionary to store all of the sound file categories
        found in the sound_directory. The sound file categories are the
        keys and the paths to the sound files are the values.

        Inputs:
            sound_directory: A string representing the path to the
            folder containing the sound files (or folders).
            file_type: A string representing the file type to search
            for. An asterik must be put in front to select all files
            that fit the specificed type.

        Returns:
            sound_folders_dict: A dictionary containing the sound 
            folders (categories) as the keys and the paths to the sound
            files as the values.
        """

        # Create a dictionary to hold folder names and their corresponding .wav files
        sound_folders_dict = {}

        for directory in os.listdir(sound_directory):
            folder_path = os.path.join(sound_directory, directory)
            
            if os.path.isdir(folder_path):
                # Find all .wav files in the folder and add them to the dictionary
                sound_folders_dict[directory] = glob.glob(os.path.join(folder_path, file_type))  

        return sound_folders_dict
    
    def play(self, sound_file: str, bg: bool=False):
        """
        Basic function to play sound.

        Inputs:
            sound_file: A string representing the sound file to be
            played.
            bg: A boolean representing whether or not to play the sound
            in the background.
        """
        print(f"Playing: {sound_file}")
        playsound(sound_file, block=bg)

    def play_sound(self, folder: str, bg: bool=False):
        if folder in self.sound_folders:
            sound_files_in_folder = self.sound_folders[folder]
            if sound_files_in_folder:
                sound_file = random.choice(sound_files_in_folder)
                self.play(sound_file, bg)

    def play_on_press(self, folder: str, pin: int=4, wings: bool=False):
        """
        Plays music on a button press.

        Inputs:
            folder: A string representing the folder in which to find
            the sound files to play.
            pin: An integer representing the pin of the button on the
            Raspberry Pi. This number is in BCM.
            wings: A boolean representing whether or not to move the 
            wings alongside the audio.
        """

        # Set up the button and create a flag
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        button_pressed = False

        # Check to make sure the given sound folder is valid
        if folder in self.sound_folders:
            # If it, look at the sound files within the folder
            sound_files_in_folder = self.sound_folders[folder]

            # If there are sound files in the folder
            if sound_files_in_folder:
                # Select a random sound file within the folder
                sound_file = random.choice(sound_files_in_folder)

                # Determine when the pin is pressed
                while not button_pressed:

                    if GPIO.input(pin) == GPIO.HIGH:
                        self.play(sound_file)
                        button_pressed = True

                        # TODO: Calculate length of sound file and make
                        # the wing movement move according to that

                        if wings: # Move the wings if we want it to
                            move_motors()