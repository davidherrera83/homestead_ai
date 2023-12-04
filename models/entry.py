from pydantic import BaseModel
from typing import List

class Entry(BaseModel):
    userQuery: List[str]
    chatGPTResponse: List[str]

class RootSchema(BaseModel):
    entries: List[Entry]