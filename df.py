from deepface import DeepFace
import config

def analyse_for_create_session():
    image_path = f'{config.path}image.jpg'
    analysis = DeepFace.analyze(image_path, actions=['gender', 'age', 'race'])
    return analysis[0]["dominant_gender"], analysis[0]["dominant_race"], analysis[0]["age"]

def analyse(token):
    image_path = f'{config.path}temp/{token}.jpg'
    analysis = DeepFace.analyze(image_path, actions=['emotion'])
    return analysis[0]["dominant_emotion"]
