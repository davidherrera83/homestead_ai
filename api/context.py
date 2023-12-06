import os
import json

from fastapi import FastAPI, HTTPException, Header
from models.entry import RootSchema
from fw import get_token

app = FastAPI()
_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_json= os.path.join(_root_dir, 'hh_context.json')

def verify_token(request_token: str):
    secret_token = get_token().token
    if request_token != secret_token:
        raise HTTPException(status_code=401, detail='Invalid token')

@app.get('/getHHContext')
def get_homestead_context(token: str = Header(None)):
    if token is None:
        raise HTTPException(status_code=401, detail='Token is missing')


    with open(_json , 'r') as file:
        json_content = file.read()
    return {"content": json_content}

@app.post('/updateHHContext')
def update_homestead_context(update: RootSchema, token: str = Header(None)):
    if token is None:
        raise HTTPException(status_code=401, detail='Token is missing')

    try:
        with open(_json, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {"entries": []}

    # Convert Entry objects to dictionaries for JSON serialization
    entries_to_add = [entry.dict() for entry in update.entries]

    # Merging Logic
    existing_data["entries"].extend(entries_to_add)

    # Save updated data back to the file
    with open(_json, 'w') as file:
        json.dump(existing_data, file, indent=4)

    return {"message": "Content updated successfully"}
