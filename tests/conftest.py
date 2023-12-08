import pytest
import uuid
import requests

from fw import Endpoint
from api.context import create_new_entry as create_entry_func


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
