import os
import json
import uuid

from fastapi import FastAPI, HTTPException, Header
from models.entry import RootSchema
from models.entry import EntryModel
from fw import get_token

app = FastAPI()
_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_json= os.path.join(_root_dir, 'hh_context.json')

def verify_token(request_token: str):
    secret_token = get_token().token
    if request_token != secret_token:
        raise HTTPException(status_code=401, detail='Invalid token')
    
def create_new_entry(user_query: list[str], chatGPT_response: list[str]) -> EntryModel:
    entry_id = str(uuid.uuid4())

    return EntryModel(
        id=entry_id,
        userQuery=user_query,
        chatGPTResponse=chatGPT_response
    )

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

    # Create a set of existing entry IDs for easy lookup
    existing_ids = {str(entry.get('id')) for entry in existing_data["entries"] if 'id' in entry}

    # Check for duplicate IDs in the update request
    for entry in update.entries:
        entry_id = str(entry.id)
        if entry_id in existing_ids:
            raise HTTPException(status_code=400, detail=f"Duplicate entry ID: {entry_id}")
        else:
            existing_ids.add(entry_id)
            entry_dict = entry.dict()
            entry_dict['id'] = entry_id  # Ensure ID is a string
            existing_data["entries"].append(entry_dict)

    # Convert all UUIDs in existing_data to strings
    for entry in existing_data["entries"]:
        if isinstance(entry.get('id'), uuid.UUID):
            entry['id'] = str(entry['id'])

    # Save updated data back to the file
    with open(_json, 'w') as file:
        json.dump(existing_data, file, indent=4)

    return {"message": "Content updated successfully"}


@app.delete('/deleteHHContext/{entry_id}')
def delete_homestead_context(entry_id: str, token: str = Header(None)):
    if token is None:
        raise HTTPException(status_code=401, detail='Token is missing')

    try:
        with open(_json, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Context file not found')

    # Find the index of the entry with the given ID
    index_to_delete = None
    for i, entry in enumerate(existing_data["entries"]):
        if entry['id'] == entry_id:
            index_to_delete = i
            break

    # Check if the entry exists
    if index_to_delete is None:
        raise HTTPException(status_code=404, detail='Entry not found')

    # Remove the entry with the given ID
    del existing_data["entries"][index_to_delete]

    # Save the updated data back to the file
    with open(_json, 'w') as file:
        json.dump(existing_data, file, indent=4)

    return {"message": "Entry deleted successfully"}
