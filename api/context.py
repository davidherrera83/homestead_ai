from fastapi import FastAPI
from models.entry import RootSchema
import os
import json

app = FastAPI()
_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_json= os.path.join(_root_dir, 'hh_context.json')

@app.get('/getHHContext')
def get_homestead_context():
    with open(_json , 'r') as file:
        json_content = file.read()
    return {"content": json_content}

@app.post('updateHHContext')
def update_homestead_context(update: RootSchema):
    # Load existing data
    try:
        with open(_json,'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {"entries": []}

    # Merging logic
    existing_data["entries"].extend(update.entries)

    # Save updated data back to the file
    with open(_json, 'w') as file:
        json.dump(existing_data, file, indent=4)

    return {"message": "Content updated successfully"}
