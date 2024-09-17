from random import randint
import config
import df
import gigachat
import tts
import base64

sessions = {}
session_token = None
# token: [message1, message2,...]

def create_session(gender, race, age):
    prompt_create = config.prompt_create.replace('%gender%', gender).replace('%race%', race).replace('%age%', str(age))
    token = str(randint(0, 1000000))
    sessions[token] = {"last_message": "", "gender": gender, "race": race, "age": age, "messages": [{"role": "user", "content": prompt_create},
                                                                                {"role": "assistant", "content": config.create_assistant}]}

    return token

def add_message(token, photo, text):
    emotion = 'не определена'
    if photo:
        emotion = df.analyse(token)
    sessions[token]["last_message"] = text
    prompt = text + f'\n\nЭмоция: {emotion}'
    print(prompt)
    sessions[token]["messages"].append({"role": "user", "content": prompt})
    assistant_answer = gigachat.do_request(sessions[token]["messages"])
    print(assistant_answer)
    sessions[token]["messages"].append({"role": "assistant", "content": assistant_answer})
    print(sessions[token]["messages"])
    tts.speak(token, assistant_answer)
    with open(f'temp/{token}.mp3', 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return assistant_answer, data
