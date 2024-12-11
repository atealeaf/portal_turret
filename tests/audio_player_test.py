from audioplayer import AudioPlayer
import time

# Playback stops when the object is destroyed (GC'ed), so save a reference to the object for non-blocking playback.
player = AudioPlayer("/home/aabc/mu_code/music/portal_song.mp3")
player.play(block=False)

try:
    while True:
        time.sleep(1)  # Sleep for 1 second
except KeyboardInterrupt:
    print("Playback interrupted.")