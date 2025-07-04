import random
import pyttsx3
import speech_recognition as sr
import yt_dlp
import os
import time
import librosa
import numpy as np
import sys

engine = pyttsx3.init()

song_data = {
    'happy': [
        'https://youtu.be/Jb_9kvrjkBY?si=3NmYKbeFZRSwDaoU', 
        'https://youtu.be/ki0Ocze98U8?si=kaIAJHh8_-TcCjCN',  
    ],
    'sad': [
        'https://www.youtube.com/watch?v=BQnxJWwAAhA&list=RDGMEMCMFH2exzjBeE_zAHHJOdxg&start_radio=1&rv=hHuG7FIKgtc',  
        'https://www.youtube.com/watch?v=jADTdg-o8i0',  
    ],
    'neutral': [
        'https://www.youtube.com/watch?v=pVytRyTnDOg&list=RDpVytRyTnDOg&start_radio=1',  
        'https://www.youtube.com/watch?v=hHuG7FIKgtc',  
    ],
    'angry': [
        'https://youtu.be/VMEXKJbsUmE?si=Kv1GThHbaJ-NHbYQ',  # Killing in the Name - Rage Against the Machine
        'https://youtu.be/dH1uaLw0IJA?si=gfmiuRraO7MedLYg',  # Break Stuff - Limp Bizkit
    ]
}

def analyze_voice_expression(audio_file):
    """
    Analyze the voice expression from the audio file and return the detected emotion.
    """
    y, sr = librosa.load(audio_file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    emotion = random.choice(['happy', 'sad', 'neutral', 'angry'])  # Replace with your model
    return emotion

def recommend_music(emotion):
    """
    Recommend a song URL based on the detected emotion.
    """
    if emotion in song_data and song_data[emotion]:
        return random.choice(song_data[emotion])
    else:
        return None

def play_music_online(video_url):
    """
    Play the YouTube video directly using yt-dlp.
    """
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info['url']
        
        os.system(f'start {audio_url}')  # Open the URL in the default web browser

    except yt_dlp.utils.DownloadError as e:
        print(f"Error: {e}")
        engine.say("Sorry, I couldn't play the recommended song.")
        engine.runAndWait()

def update_conversation(conversation_log):
    """
    Updates the conversation log with the latest conversation.
    """
    with open("conversation_log.txt", "a") as log_file:
        log_file.write(conversation_log + "\n")

def main():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Please express your mood...")
        engine.say("Please express your mood.")
        engine.runAndWait()
        audio = recognizer.listen(source)
        
        with open("user_voice.wav", "wb") as f:
            f.write(audio.get_wav_data())
    
    emotion = analyze_voice_expression("user_voice.wav")
    print(f"Detected emotion: {emotion}")
    
    update_conversation(f"User expressed mood: {emotion}")  # Log the conversation
    
    recommendation = recommend_music(emotion)
    
    if recommendation:
        engine.say("Playing music based on your mood.")
        engine.runAndWait()
        print(f"Playing: {recommendation}")
        play_music_online(recommendation)
        update_conversation(f"Playing song: {recommendation}")  # Log the conversation
        time.sleep(3)  # Adjust time as needed
        sys.exit()
    else:
        engine.say("Sorry, I couldn't find a song for your mood.")
        engine.runAndWait()
        sys.exit()

if __name__ == "__main__":
    main()
