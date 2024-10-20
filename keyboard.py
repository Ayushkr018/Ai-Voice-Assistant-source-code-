from pynput.keyboard import Key, Controller
from time import sleep
import wmi
import pyttsx3

# Initialize the keyboard controller
keyboard = Controller()

# Initialize the speech engine for voice feedback
engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    """Speak the given audio."""
    engine.say(audio)
    engine.runAndWait()

# Volume Control Functions
def volume_up(steps=5, update_conversation=None):
    """Increase the volume by a number of steps (default is 5)."""
    speak("Increasing volume, sir.")
    if update_conversation:
        update_conversation("Assistant: Increasing volume, sir.")
    for _ in range(steps):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)

def volume_down(steps=5, update_conversation=None):
    """Decrease the volume by a number of steps (default is 5)."""
    speak("Decreasing volume, sir.")
    if update_conversation:
        update_conversation("Assistant: Decreasing volume, sir.")
    for _ in range(steps):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)

def mute_volume(update_conversation=None):
    """Mute the volume."""
    speak("Muting volume, sir.")
    if update_conversation:
        update_conversation("Assistant: Muting volume, sir.")
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)

def unmute_volume(update_conversation=None):
    """Unmute the volume by toggling the mute."""
    speak("Unmuting volume, sir.")
    if update_conversation:
        update_conversation("Assistant: Unmuting volume, sir.")
    mute_volume()

# Media Playback Control Functions
def play_pause_media(update_conversation=None):
    """Play or pause the current media."""
    speak("Playing or pausing media, sir.")
    if update_conversation:
        update_conversation("Assistant: Playing or pausing media, sir.")
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)

def next_track(update_conversation=None):
    """Skip to the next track."""
    speak("Skipping to the next track, sir.")
    if update_conversation:
        update_conversation("Assistant: Skipping to the next track, sir.")
    keyboard.press(Key.media_next)
    keyboard.release(Key.media_next)

def previous_track(update_conversation=None):
    """Go to the previous track."""
    speak("Playing the previous track, sir.")
    if update_conversation:
        update_conversation("Assistant: Playing the previous track, sir.")
    keyboard.press(Key.media_previous)
    keyboard.release(Key.media_previous)

def stop_media(update_conversation=None):
    """Stop the current media."""
    speak("Stopping media, sir.")
    if update_conversation:
        update_conversation("Assistant: Stopping media, sir.")
    keyboard.press(Key.media_stop)
    keyboard.release(Key.media_stop)

# Brightness Control (Windows-specific using WMI)
def set_brightness(level, update_conversation=None):
    """Set the brightness to a specific level (0 to 100)."""
    speak(f"Setting brightness to {level} percent, sir.")
    if update_conversation:
        update_conversation(f"Assistant: Setting brightness to {level} percent, sir.")
    c = wmi.WMI(namespace='wmi')
    methods = c.WmiMonitorBrightnessMethods()[0]
    methods.WmiSetBrightness(level, 0)  # Set brightness with level (0-100)

def increase_brightness(step=10, update_conversation=None):
    """Increase the brightness by a specified step (default is 10%)."""
    c = wmi.WMI(namespace='wmi')
    current_brightness = c.WmiMonitorBrightness()[0].CurrentBrightness
    new_brightness = min(current_brightness + step, 100)
    set_brightness(new_brightness, update_conversation)

def decrease_brightness(step=10, update_conversation=None):
    """Decrease the brightness by a specified step (default is 10%)."""
    c = wmi.WMI(namespace='wmi')
    current_brightness = c.WmiMonitorBrightness()[0].CurrentBrightness
    new_brightness = max(current_brightness - step, 0)
    set_brightness(new_brightness, update_conversation)

def set_brightness_50(update_conversation=None):
    """Set the brightness directly to 50%."""
    set_brightness(50, update_conversation)

# Skip Forward and Backward in Media (10 seconds)
def skip_forward_10s(update_conversation=None):
    """Skip forward in the media by 10 seconds."""
    speak("Skipping forward 10 seconds, sir.")
    if update_conversation:
        update_conversation("Assistant: Skipping forward 10 seconds, sir.")
    for _ in range(2):
        keyboard.press(Key.media_next)
        keyboard.release(Key.media_next)
        sleep(0.1)

def skip_backward_10s(update_conversation=None):
    """Skip backward in the media by 10 seconds."""
    speak("Skipping backward 10 seconds, sir.")
    if update_conversation:
        update_conversation("Assistant: Skipping backward 10 seconds, sir.")
    for _ in range(2):
        keyboard.press(Key.media_previous)
        keyboard.release(Key.media_previous)
        sleep(0.1)
