import time
import datetime
import ctypes
import sys
import os
from plyer import notification
import pyttsx3
import psutil

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def speak(message):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty("rate", 150)
    engine.say(message)
    engine.runAndWait()

def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

def close_apps():
    apps_to_close = ["WhatsApp", "chrome", "Instagram", "wmplayer"]  # Media Player is 'wmplayer'
    
    for proc in psutil.process_iter(['pid', 'name']):
        if any(app.lower() in proc.info['name'].lower() for app in apps_to_close):
            try:
                proc.terminate()  # Gracefully terminate the app
                speak(f"{proc.info['name']} has been closed.")
            except Exception as e:
                print(f"Error closing {proc.info['name']}: {e}")

def start_focus_mode():
    if is_admin():
        current_time = datetime.datetime.now().strftime("%H:%M")
        stop_time = input("Enter stop time in format [HH:MM]: ")
        current_time_float = float(current_time.replace(":", "."))
        stop_time_float = float(stop_time.replace(":", "."))
        focus_time = round(stop_time_float - current_time_float, 3)

        host_path = r'C:\Windows\System32\drivers\etc\hosts'
        redirect = '127.0.0.1'

        website_list = ["www.facebook.com", "facebook.com", "www.instagram.com", "instagram.com", "www.youtube.com", "youtube.com"]

        if current_time_float < stop_time_float:
            with open(host_path, "r+") as file:
                content = file.read()
                for website in website_list:
                    if website not in content:
                        file.write(f"{redirect} {website}\n")
                notify("Focus Mode Activated", "Websites are blocked.")
                speak("Focus mode started. Websites are blocked.")
                close_apps()  # Close the specific apps
                print("FOCUS MODE TURNED ON!")

            # Get the session start time in a datetime format
            session_start_time = datetime.datetime.now()

            while True:
                # Notification every minute
                time.sleep(60)
                notify("Focus Mode", "You are still in focus mode.")

                current_time = datetime.datetime.now().strftime("%H:%M")
                if float(current_time.replace(":", ".")) >= stop_time_float:
                    # Unblock websites
                    with open(host_path, "r+") as file:
                        content = file.readlines()
                        file.seek(0)
                        for line in content:
                            if not any(website in line for website in website_list):
                                file.write(line)
                        file.truncate()
                    notify("Focus Mode Ended", "Websites are unblocked.")
                    speak("Focus mode ended. Websites are unblocked.")
                    print("Websites are unblocked!")

                    # Log focus session with start time, end time, and focus duration
                    session_end_time = datetime.datetime.now()
                    with open("focus.txt", "a") as file:
                        file.write(f"Focus session: {focus_time} hours, Date: {session_start_time.strftime('%Y-%m-%d %H:%M')}\n")
                    break

    else:
        # Restart as admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

start_focus_mode()
