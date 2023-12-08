from pydantic import BaseModel, Field, UUID4
from typing import List
import uuid

class EntryModel(BaseModel):
    id: str  
    userQuery: List[str]
    chatGPTResponse: List[str]

class RootSchema(BaseModel):
    entries: List[EntryModel]