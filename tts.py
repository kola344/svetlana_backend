from gtts import gTTS
import os
import subprocess
from mutagen.mp3 import MP3
import config

def speak(token, text):
    tts = gTTS(text=text, lang='ru')
    tts.save(f"{config.path}temp/{token}.mp3")
    audio = MP3(f"{config.path}temp/{token}.mp3")
    duration = audio.info.length
    if duration == 0:
        duration = 1
    return duration
