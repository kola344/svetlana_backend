from gtts import gTTS
import os
import subprocess

def speak(token, text):
    tts = gTTS(text=text, lang='ru')
    tts.save(f"temp/{token}.mp3")
    subprocess.run(["afplay", f"temp/{token}.mp3"])