import os
import shutil
import pyttsx3
from time import sleep

def speak(text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)  # Female voice
    engine.setProperty("rate", 200)
    engine.say(text)
    engine.runAndWait()

def voice_controlled_file_manager(query, update_conversation):
    query = query.lower()

    # 1. Open File Manager
    if "open file manager" in query or "launch explorer" in query:
        try:
            os.system("explorer")
            speak("File Manager opened successfully.")
            update_conversation("Assistant: File Manager opened successfully.")
        except Exception as e:
            speak("Unable to open File Manager.")
            update_conversation(f"Assistant: Error opening File Manager - {e}")

    # 2. Search by file extension (e.g., .py)
    elif "search" in query and "." in query:
        try:
            ext = query.split("search for")[-1].strip()
            if not ext.startswith("."):
                ext = "." + ext
            base_path = os.path.expanduser("~")
            result_files = []
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.endswith(ext):
                        result_files.append(os.path.join(root, file))
            if result_files:
                speak(f"Found {len(result_files)} files with {ext} extension.")
                update_conversation(f"Assistant: Found these files:\n" + "\n".join(result_files[:5]))
            else:
                speak(f"No files found with {ext} extension.")
                update_conversation(f"Assistant: No files found with {ext} extension.")
        except Exception as e:
            speak("An error occurred while searching.")
            update_conversation(f"Assistant: Error - {e}")

    # 3. Create a folder
    elif "create folder" in query:
        try:
            speak("What name should I give the folder?")
            folder_name = input("Speak or type folder name: ")
            path = os.path.join(os.path.expanduser("~"), folder_name)
            os.makedirs(path, exist_ok=True)
            speak(f"Folder {folder_name} created.")
            update_conversation(f"Assistant: Folder '{folder_name}' created.")
        except Exception as e:
            speak("Unable to create folder.")
            update_conversation(f"Assistant: Error creating folder - {e}")

    # 4. Delete a file/folder
    elif "delete" in query:
        speak("Please provide the full name of the file or folder to delete.")
        target = input("Speak or type full path to delete: ")
        try:
            if os.path.isdir(target):
                shutil.rmtree(target)
                speak("Folder deleted.")
                update_conversation(f"Assistant: Folder deleted.")
            elif os.path.isfile(target):
                os.remove(target)
                speak("File deleted.")
                update_conversation(f"Assistant: File deleted.")
            else:
                speak("File or folder not found.")
                update_conversation(f"Assistant: Target not found.")
        except Exception as e:
            speak("Deletion failed.")
            update_conversation(f"Assistant: Error deleting - {e}")

    # 5. Rename a file or folder
    elif "rename" in query:
        speak("What is the current path of the file or folder?")
        src = input("Current path: ")
        speak("What should be the new name?")
        new_name = input("New name: ")
        try:
            base = os.path.dirname(src)
            dst = os.path.join(base, new_name)
            os.rename(src, dst)
            speak("Renamed successfully.")
            update_conversation("Assistant: Renamed successfully.")
        except Exception as e:
            speak("Rename failed.")
            update_conversation(f"Assistant: Error renaming - {e}")

    else:
        update_conversation("Assistant: Sorry, I didn't understand the file command.")
