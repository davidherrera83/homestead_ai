import logging

from pydantic import BaseModel, validator

logger = logging.getLogger(__name__)

class TokenModel(BaseModel):
    token: str