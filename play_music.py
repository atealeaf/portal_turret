"""
A Python program to play music on the Rapsberry Pi 4 Model B.

This creates a class to store music files and play them when commanded. 
It also allows for movement alongside the sounds played.
"""

import os
import glob
import RPi.GPIO as GPIO
import time
from audioplayer import AudioPlayer 
# Import sound detection functions
from sound_sensing import read_sound 
from mutagen.mp3 import MP3
from ir_receiver import read_ir
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class PlayMusic:
    """
    Create a class to play music on the Raspberry Pi 4 with Mu Code.

    When Mu Code is installed, it automatically creates some folders.
    Of those folders, we are interested in `music` and `sounds`. For
    this program to work, music files must be in `music`; no subfolders
    are allowed. The allowed file types are listed below.
    """
    # List of the allowed music file types to play
    FILE_TYPES = [".wav", ".mp3", ".ogg"]

    def __init__(self, music_directory: str):
        """
        Initialize variables to store within the class.

        This includes all of the music files stored on the Raspberry Pi
        via Mu.

        Inputs:
            music_directory: A string representing the path to the
            folder containing the music files.
        """
        # Save the music directory path
        self.music_directory = music_directory
        # Paths and names of all the music files
        self.music_file_paths = self.get_music_files(music_directory)
        self.music_file_names = self.get_music_files(
            music_directory, False)

    def get_music_files(self, music_directory: str, path: bool=True):
        """
        Gets the music files from the directory provided.

        Inputs:
            music_directory: A string representing the music directory
            to locate the music files in.
            path: A boolean representing whether or not to express the
            music files with their full path or just the file name.

        Returns:
            music_files: A list containing strings representing the
            paths to all the music files in music_directory.
            song_names: A list containing strings representing the
            names of all the music files in music_directory.
        """
        # Create a list to store all of the music files
        music_files = [] 
        # This for loop checks for multiple different file types
        for file_type in self.FILE_TYPES:
            pattern = os.path.join(
                music_directory, "**", f"*{file_type}")
            music_files.extend(glob.glob(pattern, recursive=True))
        # If path is set to True, a list of the paths will be returned
        if path:
            return music_files
        # If path is set to False, a list of file names is returned
        else:
            song_names = [
                os.path.basename(file) for file in music_files]
            return song_names

    def dance_to_song(self, song: str, pin: int=4, dance: bool=True):
        """
        Plays a song when a button is pressed. The motors will move
        based on audio input, which is detected via a sound sensor and
        ADC module.

        Inputs:
            song: A string representing the path of the song to be
            played.
            pin: An integer representing the pin of the button on the
            Raspberry Pi. This number is in BCM.
            dance: A boolean representing whether or not to make motors
            move in time with the song via sound sensors.
        """

        # Set up the pin and a flag
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        button_pressed = False
        
        # Determine when the pin is pressed
        while not button_pressed:
            if GPIO.input(pin) == GPIO.HIGH:
                button_pressed = True

                player = AudioPlayer(song)
                player.play(block=False)

                # This allows the song to keep playing when block is 
                # False, but we can still interrupt it.
                try:
                    while True:
                        time.sleep(0.1)
                        if dance:
                            # Read the sound value and move motors if
                            # it is past the threshold.
                            read_sound()
                except KeyboardInterrupt:
                    print("Playback interrupted.")

    def cycle_songs_button(self, pin: int = 4, dance: bool = True):
        """
        Cycles through songs in the music folder provided.

        The next song will automatically play when the current song
        ends. Alternatively, pressing the input button will force the
        next song to play, stopping the current song. If `dance` is set
        to True, then sound sensors will command the motors to move. 

        Inputs: 
            pin: An integer representing the pin of the button on the
            Raspberry Pi. This number is in BCM.
            dance: A boolean representing whether or not to make motors
            move in time with the song via sound sensors.
        """
        # Set up the pin and a flag
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        button_pressed = False
        
        # Rename the music file paths lists to folder
        folder = self.music_file_paths
        press_count = 0 # Track which song to play
        song_ended = False # Tell if the song has ended

        while True:

            # Check to see if the next song button was pressed or if 
            # the current song has ended.
            if GPIO.input(pin) == GPIO.HIGH and (
                not button_pressed or song_ended):

                # A modulus is used to account for press counts past
                # the song list length
                song_index = press_count % len(folder)
                song = folder[song_index] # Get the song
                # Get the song length
                song_length = self.get_song_length(song)

                # Because the button has been pressed, set it to true
                button_pressed = True

                # Print the song that is playing and its duration
                print(f"Playing: {song} ({song_length:.2f} seconds)")
                player = AudioPlayer(song) # Play the song
                player.play(block=False) # Let other processes run

                # Start a timer for the song length
                start_time = time.time()
                song_ended = False

                while not song_ended:
                    # This tracks how much time has passed since the
                    # song's start.
                    current_time = time.time()
                    elapsed_time = current_time - start_time

                    if dance:
                        # Read the sound value and move motors if it
                        # is past the threshold
                        read_sound(debug=True)

                    # Check if the song has finished or if the button
                    # is pressed again
                    if elapsed_time >= song_length or (
                        GPIO.input(pin) == GPIO.HIGH):
                        print("Song interrupted or finished.")
                        player.stop()  # Stop the player if needed
                        song_ended = True  # Mark the song as ended
                        break # Break out of this loop

                    time.sleep(0.1)  # Sleep to prevent busy waiting

                # After the song ends, increment the press count for
                # the next song
                press_count += 1

            elif GPIO.input(pin) == GPIO.LOW:
                # Reset the button pressed flag when released
                button_pressed = False 

    def get_song_length(self, song_path: str):
        """
        Gets the length of the song provided.

        Inputs:
            song_path: A string representing the path to the song we
            want to get the length of.
        
        Returns:    
            audio.info.length: A float representing the length of the
            song in seconds.
        """
        audio = MP3(song_path)
        return audio.info.length

    
    def ir_play(self, client, dance: bool=True):
        """
         Cycles through songs in the music folder provided.

        The next song will automatically play when the current song
        ends. If `dance` is set to True, then sound sensors will 
        command the motors to move. 

        This was made to work with an IR remote featuring a play/pause
        button, a next button, a previous button, a mode button, and
        a power button. Pressing each button will elicit a different
        response corresponding to the name of the button.

        Inputs: 
            client: An LIRC connection class from the LIRC library.
            This refers to the IR remote being used.
            dance: A boolean representing whether or not to make motors
            move in time with the song via sound sensors.

        Returns:
            new_signal: A string representing the signal corresponding
            to the key pressed on the IR remote.
        """
        button_pressed = False
        folder = self.music_file_paths
        song_index = 0  # Track which song to play
        song_ended = True  # Tell if the song has ended
        pause = False  # Tell if the song is paused or not

        # Variables so that pressing the button once doesn't register
        # multiple times.
        debounce_time = 0.5 
        last_signal_time = 0
        new_signal = None  # Initialize new_signal

        # Create an event to signal the sound thread to stop
        stop_event = threading.Event()

        def sound_reader():
            """
            Thread function to continuously read sound if dance is set
            to `True`.
            """
            # Check if the stop event is set
            while not stop_event.is_set(): 
                if dance:
                    read_sound() # Read the sound if dance is `True`
                time.sleep(0.1)  # Sleep to prevent busy waiting

        # Start the sound reader thread
        sound_thread = threading.Thread(target=sound_reader)
        sound_thread.daemon = True 
        sound_thread.start()

        while True:

            # Check to make sure that the song hasn't ended or a button
            # hasn't been pressed
            if not button_pressed or song_ended:
                
                # Get the song and song length
                song = folder[song_index]
                song_length = self.get_song_length(song) 

                # Set button pressed to true
                button_pressed = True
                print(f"Playing: {song} ({song_length:.2f} seconds)")
                player = AudioPlayer(song)  # Play the song
                player.play(block=False)  # Let other processes run

                # This is to check when the song ends
                song_start_time = time.time()
                song_ended = False

                # Other tasks run while the song hasn't ended
                while not song_ended:

                    # Check to make sure the song hasn't ended
                    song_current_time = time.time()
                    song_elapsed_time = (
                        song_current_time - song_start_time)

                    # Check for IR signals
                    new_signal = read_ir(client)
                    current_time = time.time()
                    elapsed_time = current_time - last_signal_time

                    # Check if there is a new signal from the IR remote
                    # and it is not on cooldown.
                    if new_signal and elapsed_time > debounce_time:

                        # Check if power or mode is pressed
                        if (new_signal == "KEY_MODE") or (
                            new_signal == "KEY_POWER"):
                            player.stop()  # Stop the player if needed
                            # Signal the sound thread to stop
                            stop_event.set()
                            # Wait for the thread to finish
                            sound_thread.join(timeout=0.5) 
                            return new_signal
                        
                         # If the key is pauseplay, pause or play
                        elif new_signal == "KEY_PLAYPAUSE":
                            if pause:
                                player.resume()
                                pause = False
                            else:
                                player.pause()
                                pause = True
                        # Check if the song naturally ends or if next
                        # song or previous song is pressed.
                        elif song_elapsed_time >= song_length or (
                            new_signal in (
                                "KEY_NEXTSONG", "KEY_PREVIOUSSONG")):
                            player.stop()
                            song_ended = True

                            # If next song was pressed, play the next
                            # song or wrap around.
                            if new_signal == "KEY_NEXTSONG":
                                song_index = (song_index + 1) % len(
                                    folder)
                            # If previous song was pressed, play the
                            # previous song or wrap around.
                            elif new_signal == "KEY_PREVIOUSSONG":
                                song_index = (song_index - 1) % len(
                                    folder)
                            break  # Stop the playing loop
            
            # If there was a new signal, return it
            if new_signal in ("KEY_MODE", "KEY_POWER"):
                player.stop()
                stop_event.set()  # Signal the sound thread to stop
                # Wait for the thread to finish
                sound_thread.join(timeout=0.5)  
                return new_signal