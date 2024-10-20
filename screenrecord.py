import cv2
import pyautogui
import numpy as np
import time

def start_screen_recording(output_file="screen_recording.mp4", duration=10, fps=12):
    """
    Records the screen for a specific duration and saves it as a video file.

    Parameters:
    - output_file: Name of the output video file.
    - duration: Duration of the recording in seconds.
    - fps: Frames per second for the video.
    """
    
    # Get the screen resolution
    screen_size = pyautogui.size()

    # Create a VideoWriter object to save the recording
    fourcc = cv2.VideoWriter_fourcc(*"XVID")  # Codec for video format
    out = cv2.VideoWriter(output_file, fourcc, fps, screen_size)

    # Record the screen for the given duration
    start_time = time.time()
    while True:
        # Take a screenshot
        img = pyautogui.screenshot()

        # Convert the image to a NumPy array for OpenCV
        frame = np.array(img)

        # Convert from RGB (PyAutoGUI) to BGR (OpenCV)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Write the frame to the video file
        out.write(frame)

        # Break the loop after the given duration
        if time.time() - start_time > duration:
            break

    # Release the VideoWriter object
    out.release()

    print(f"Screen recording saved as {output_file}")

# To use this in your voice assistant:
if __name__ == "__main__":
    # Start screen recording for 10 seconds (adjust duration as needed)
    start_screen_recording(output_file="screen_record.mp4", duration=10, fps=12)
