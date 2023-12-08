import pytest
import uuid
import requests

from fw import Endpoint
from api.context import create_new_entry as create_entry_func


@pytest.fixture
def create_entry():
    user_query = ["test query"]
    chatGPT_response = ["test response"]
    entry = create_entry_func(user_query, chatGPT_response)
    return entry.id


@pytest.fixture
def duplicate_entry():
    url = Endpoint.update_context_url
    headers = Endpoint.headers
    new_entry = {
        "id": str(uuid.uuid4()),
        "userQuery": ["test query"],
        "chatGPTResponse": ["test response"]
    }
    response = requests.post(url, json={"entries": [new_entry]}, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        return response_json.get('id')
    else:
        raise ValueError(f"Failed to create duplicate entry. Status code: {response.status_code}")


