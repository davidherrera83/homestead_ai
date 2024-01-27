import json
import os

from models.secret import SecretModel

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))



def get_secret() -> SecretModel:
    """
    Get the TokenModel from secrets.json
    """
    with open(_ROOT_DIR + '/secrets.json', 'r') as json_file:
        _json = json.loads(json_file.read())

        return SecretModel(**_json)

class Endpoint:
        base_url = "https://api.openai.com/v1"
        assistant_id = get_secret().assistant_id
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_secret().api_key}",
            "OpenAI-Beta": "assistants=v1"
        }
        file_headers = {
            "Authorization": f"Bearer {get_secret().api_key}",
        }
        threads = f"{base_url}/threads"
        files = f"{base_url}" +"/files"

class Files:
        hh_context = '/Users/david.herrera/dev/homestead_ai/hh_context.json'
        file_id = get_secret().file_id