from pydantic import BaseModel
from typing import List


class EntryModel(BaseModel):
    id: str  
    userQuery: List[str]
    chatGPTResponse: List[str]

class RootSchema(BaseModel):
    entries: List[EntryModel] 