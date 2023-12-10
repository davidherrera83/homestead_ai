import os
import json
import uuid
import logging

from uuid import UUID
from fastapi import FastAPI, HTTPException, Header
from models.entry import RootSchema
from models.entry import EntryModel
from fw import get_token

# This configuration logs the timestamp, logger name, log level, and message.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_json = os.path.join(_root_dir, 'hh_context.json')

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
    logger.info("Received request for get_homestead_context with token: %s", token)
    try:
        if token is None:
            raise HTTPException(status_code=401, detail='Token is missing')

        with open(_json, 'r') as file:
            json_content = file.read()
        return {"content": json_content}
    except Exception as e:
        logger.error("Error in get_homestead_context: %s", str(e))
        raise

def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

@app.post('/updateHHContext')
def update_homestead_context(update: RootSchema, token: str = Header(None)):
    logger.info("Received request for update_homestead_context with token: %s", token)
    try:
        if token is None:
            raise HTTPException(status_code=401, detail='Token is missing')

        try:
            with open(_json, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {"entries": []}

        existing_ids = {str(entry.get('id')) for entry in existing_data["entries"] if 'id' in entry}

        for entry in update.entries:
            entry_id = str(entry.id)
            if not is_valid_uuid(entry_id):
                raise HTTPException(status_code=422, detail=f"Invalid ID format: {entry_id}")

            if entry_id in existing_ids:
                raise HTTPException(status_code=400, detail=f"Duplicate entry ID: {entry_id}")
            else:
                existing_ids.add(entry_id)
                entry_dict = entry.dict()
                entry_dict['id'] = entry_id
                existing_data["entries"].append(entry_dict)

        for entry in existing_data["entries"]:
            if isinstance(entry.get('id'), uuid.UUID):
                entry['id'] = str(entry['id'])

        with open(_json, 'w') as file:
            json.dump(existing_data, file, indent=4)

        logger.info("Homestead context updated successfully")
        return {"message": "Content updated successfully"}
    except Exception as e:
        logger.error("Error in update_homestead_context: %s", str(e))
        raise


@app.delete('/deleteHHContext/{entry_id}')
def delete_homestead_context(entry_id: str, token: str = Header(None)):
    logger.info("Received request for delete_homestead_context with token: %s", token)
    try:
        if token is None:
            raise HTTPException(status_code=401, detail='Token is missing')

        try:
            with open(_json, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail='Context file not found')

        index_to_delete = None
        for i, entry in enumerate(existing_data["entries"]):
            if entry['id'] == entry_id:
                index_to_delete = i
                break

        if index_to_delete is None:
            raise HTTPException(status_code=404, detail='Entry not found')

        del existing_data["entries"][index_to_delete]

        with open(_json, 'w') as file:
            json.dump(existing_data, file, indent=4)

        return {"message": "Entry deleted successfully"}
    except Exception as e:
        logger.error("Error in delete_homestead_context: %s", str(e))
        raise