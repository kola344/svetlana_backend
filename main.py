from fastapi import FastAPI, HTTPException, Request
from models import session
import sessions
import base64
import traceback
import df

app = FastAPI()
this_first = []

@app.get("/")
async def index_page():
    return {"message": "Hello World"}

# @app.exception_handler(HTTPException)
# async def custom_http_exception_handler(request, exc):
#     print(f"Ошибка {exc.status_code}: {exc.detail}")

@app.post('/create_session')
async def create_session_page(request: Request):
    data = await request.json()
    photo = data["photo"]
    try:
        image_data = photo
        if "base64" in image_data:
            image_data = image_data.split("base64,")[1].replace("\n", "").replace(" ", "").replace("\r", "")
        missing_padding = len(image_data) % 4
        if missing_padding:
            image_data += "=" * (4 - missing_padding)
        image_bytes = base64.b64decode(image_data)
        with open(f"image.jpg", "wb") as f:
            f.write(image_bytes)
        gender, race, age = df.analyse_for_create_session()
        token = sessions.create_session(gender, race, age)
        return {"status": True, "token": token}
    except:
        traceback.print_exc()
        return {"status": False, "token": "err"}

@app.post('/send_request')
async def send_request_page(request: Request):
    if len(this_first) == 0:
        this_first.append(True)
        return {"status": True}
    data = await request.json()
    try:
        photo = data["photos"]
    except:
        photo = None
    if data["token"] == '' or data["token"] is None or data["token"] == "123":
        token = sessions.session_token
    else:
        token = data["token"]
    text = data["text"]
    if text == "" or text == sessions.sessions[token]["last_message"]:
        return {"status": True}
    try:
        image_data = photo
        if "base64" in image_data:
            image_data = image_data.split("base64,")[1].replace("\n", "").replace(" ", "").replace("\r", "")
        missing_padding = len(image_data) % 4
        if missing_padding:
            image_data += "=" * (4 - missing_padding)
        image_bytes = base64.b64decode(image_data)
        with open(f"temp/{token}.jpg", "wb") as f:
            f.write(image_bytes)
        response, audio_data = sessions.add_message(token, True, text)
        print(response)
        return {"status": True, "text": response, "audio": audio_data}
    except:
        # traceback.print_exc()
        try:
            response, audio_data = sessions.add_message(token, False, text)
            return {"status": True, "text": response, "audio": audio_data}
        except:
            traceback.print_exc()
        return {"status": False}

@app.on_event("startup")
async def startup():
    token = sessions.create_session("male", "european", 18)
    sessions.session_token = token


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)