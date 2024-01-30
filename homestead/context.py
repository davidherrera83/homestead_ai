import os
import json
import uuid

from models.entry import RootSchema
from models.entry import EntryModel
from fw import Files

class Homestead:
    _root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _json = os.path.join(_root_dir, 'hh_context.json')

    def create_new_entry(self, user_query: list[str], chatGPT_response: list[str]) -> EntryModel:
        entry_id = str(uuid.uuid4())
        return EntryModel(
            id=entry_id,
            userQuery=user_query,
            chatGPTResponse=chatGPT_response
        )
    
    def parse_response(self, user_query, messages: list):
        chatGPT_response = None

        for message in messages:
            if message.role == "assistant":
                for content in message.content:
                    if content.type == 'text':
                        chatGPT_response = content.text.value
                        break
            if chatGPT_response:
                break

        if chatGPT_response is not None:
            return {
                "id": str(uuid.uuid4()),
                "userQuery": [user_query], 
                "chatGPTResponse": [chatGPT_response]
            }

        return None

    def update_homestead_context(self, update: RootSchema):
        try:
            with open(self._json, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {"entries": []}
        except json.JSONDecodeError:
            raise ValueError("Error decoding JSON from file")

        existing_ids = {str(entry.get('id')) for entry in existing_data["entries"] if 'id' in entry}
        for entry in update.entries:
            entry_id = str(entry.id)
            if entry_id in existing_ids:
                raise ValueError(f"Duplicate entry ID: {entry_id}")
            else:
                    existing_ids.add(entry_id)
                    entry_dict = entry.model_dump()
                    entry_dict['id'] = entry_id
                    existing_data["entries"].append(entry_dict)

        for entry in existing_data["entries"]:
            if isinstance(entry.get('id'), uuid.UUID):
                entry['id'] = str(entry['id'])

        with open(self._json, 'w') as file:
            json.dump(existing_data, file, indent=4)

    def delete_entry_by_id(self, entry_id: str):
        try:
            with open(self._json, 'r') as file:
                data = json.load(file)
                entries = data.get("entries", [])
        except FileNotFoundError:
            raise FileNotFoundError("The JSON file does not exist.")
        except json.JSONDecodeError:
            raise ValueError("Error decoding JSON from file.")

        data["entries"] = [entry for entry in entries if entry.get('id') != entry_id]

        with open(self._json, 'w') as file:
            json.dump(data, file, indent=4)

        return f"Entry with ID {entry_id} has been deleted."
    
    def update_file_id_in_secrets(self, new_file_id: str):
        try:
            with open(f'{Files.secrets}', 'r') as file:
                secrets_data = json.load(file)

            secrets_data['file_id'] = new_file_id

            with open(f'{Files.secrets}', 'w') as file:
                json.dump(secrets_data, file, indent=4)
        except Exception as e:
            print(f"Error updating secrets.json: {e}")