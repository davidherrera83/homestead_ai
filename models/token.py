import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)

class TokenModel(BaseModel):
    token: str
    api_key: str