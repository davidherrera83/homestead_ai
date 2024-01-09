import pytest
import uuid
import requests

from fw import Endpoint, get_token
from services.open_ai import Openai


@pytest.fixture
def create_entry():
    url = Endpoint.update_context_url
    headers = Endpoint.headers
    entry_id = str(uuid.uuid4())
    entry = {
        "id": entry_id,
        "userQuery": ["test query"],
        "chatGPTResponse": ["test response"]
    }
    response = requests.post(url, json={"entries": [entry]}, headers=headers)
    if response.status_code == 200:
        return entry_id
    else:
        raise ConnectionError("Response was not OK: " + str(response.content))


@pytest.fixture
def token():
    _token_model = get_token()

    return _token_model


@pytest.fixture
def openai(token):
    _openai = Openai(token)

    return _openai
