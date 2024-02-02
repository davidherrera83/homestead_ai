import os
import json
import uuid
import time

from services.open_ai import Openai
from models.entry import RootSchema
from models.entry import EntryModel
from fw import Files, get_secret


class Homestead:
    _root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _json = os.path.join(_root_dir, 'hh_context.json')
    _api_key = get_secret().api_key
    _openai = Openai()

    def create_new_entry(self, user_query: list[str], chatGPT_response: list[str]) -> EntryModel:
        entry_id = str(uuid.uuid4())
        return EntryModel(
            id=entry_id,
            userQuery=user_query,
            chatGPTResponse=chatGPT_response
        )


def parse_response(self, user_query: str, messages: list, thread_id: str):
    print("Parsing messages:", messages)  # Debugging print
    chatGPT_response = None

    for message in messages:
        # Ensure that 'message' is the correct type and has a 'role' attribute
        if hasattr(message, 'role') and message.role == "assistant":
            for content in message.content:
                if hasattr(content, 'type') and content.type == 'text':
                    chatGPT_response = content.text.value
                    break
            if chatGPT_response:
                break

    if chatGPT_response is not None:
        return {
            "id": str(uuid.uuid4()),
            "userQuery": [user_query],
            "chatGPTResponse": [chatGPT_response],
            "thread_id": thread_id
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

    existing_ids = {str(entry.get('id'))
                    for entry in existing_data["entries"] if 'id' in entry}
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

    data["entries"] = [
        entry for entry in entries if entry.get('id') != entry_id]

    with open(self._json, 'w') as file:
        json.dump(data, file, indent=4)

    return f"Entry with ID {entry_id} has been deleted."


def conversation(self, user_query: str, thread_id=None, timeout: int = 5, max_wait_time: int = 60):
    start_time = time.time()

    if thread_id is None:
        thread_id = self._openai.create_thread()
        self.update_thread_id_in_secrets(thread_id)

    self._openai.create_message(user_query, thread_id)
    run_id = self._openai.create_run(thread_id)

    while True:
        if time.time() - start_time > max_wait_time:
            raise TimeoutError("Exceeded maximum wait time for response")

        status = self._openai.retrieve_run(thread_id, run_id)
        if status == "completed":
            break
        elif status == "failed":
            raise Exception("Run failed")
        else:
            time.sleep(timeout)

    messages_response = self._openai.list_messages(thread_id)
    return messages_response, thread_id


def get_thread_id(self):
    secrets_file_path = os.path.join(os.path.dirname(__file__), "secrets.json")
    try:
        with open(secrets_file_path, 'r') as file:
            secrets_data = json.load(file)
        return secrets_data.get('thread_id')
    except Exception as e:
        print(f"Error reading thread_id from secrets.json: {e}")
        return None


def update_thread_id_in_secrets(self, new_thread_id: str):
    secrets_file_path = os.path.join(os.path.dirname(__file__), "secrets.json")
    try:
        with open(secrets_file_path, 'r') as file:
            secrets_data = json.load(file)

        secrets_data['thread_id'] = new_thread_id

        with open(secrets_file_path, 'w') as file:
            json.dump(secrets_data, file, indent=4)

        print("Updated thread_id in secrets.json successfully.")
    except Exception as e:
        print(f"Error updating secrets.json: {e}")


def process_response_and_update_context(self, user_query, response, thread_id):
    assistant_response = self.parse_response(user_query, response, thread_id)
    if assistant_response:
        entry = EntryModel(**assistant_response)
        root_schema = RootSchema(entries=[entry])
        self.update_homestead_context(root_schema)
    return assistant_response
