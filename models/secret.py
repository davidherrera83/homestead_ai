from pydantic import BaseModel

class SecretModel(BaseModel):
    api_key: str
    assistant_id: str
    file_id: str
    thread_id: str