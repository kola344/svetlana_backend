from deepface import DeepFace

def analyse_for_create_session():
    image_path = f'image.jpg'
    analysis = DeepFace.analyze(image_path, actions=['gender', 'age', 'race'])
    return analysis[0]["dominant_gender"], analysis[0]["dominant_race"], analysis[0]["age"]

def analyse(token):
    image_path = f'temp/{token}.jpg'
    analysis = DeepFace.analyze(image_path, actions=['emotion'])
    return analysis[0]["dominant_emotion"]
