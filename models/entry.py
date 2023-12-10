import logging

from pydantic import BaseModel, validator
from typing import List

logger = logging.getLogger(__name__)

class EntryModel(BaseModel):
    id: str  
    userQuery: List[str]
    chatGPTResponse: List[str]

class RootSchema(BaseModel):
    entries: List[EntryModel]