import json
import os

from models.token import TokenModel

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_token() -> TokenModel:
    """
    Get the TokenModel from secrets.json
    """
    with open(_ROOT_DIR + '/secrets.json', 'r') as json_file:
        _json = json.loads(json_file.read())

        return TokenModel(**_json)

class Endpoint:
    base_url = "https://api.openai.com/v1"
    assistant_id = "asst_b6lo4yIzwGpyGcUrwbVpQkB5"
    file_id = "file-1IWyqznJRKnfvRBwV4esVbuz"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_token().api_key}",
        "OpenAI-Beta": "assistants=v1"
    }
    file_headers = {
        "Authorization": f"Bearer {get_token().api_key}",
    }
    threads = f"{base_url}/threads"
    files = "https://api.openai.com/v1/files"
