from pydantic import BaseModel

class send_request(BaseModel):
    text: str
    token: str
    photos: str
