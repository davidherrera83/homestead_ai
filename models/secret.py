import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)

class SecretModel(BaseModel):
    api_key: str
    assistant_id: str
    file_id: str