import requests
import os.path
import uuid

from os import path
from fw import get_token, Endpoint
from api.context import create_new_entry

herrera_homestead_file = 'hh_context.json'

def test_json_file_exists():
    assert path.exists(herrera_homestead_file)

def test_json_file_not_empty():
    assert os.stat(herrera_homestead_file).st_size is not 0

def test_get_homestead_context():
    url = Endpoint.get_context_url
    headers = Endpoint.headers
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def test_create_new_entry():
    # Create a new entry
    user_query = ["test query"]
    chatGPT_response = ["test response"]
    new_entry = create_new_entry(user_query, chatGPT_response)
    
    # Check if the new entry is created with the correct attributes
    assert isinstance(new_entry.id, str)
    assert new_entry.userQuery == user_query
    assert new_entry.chatGPTResponse == chatGPT_response


def test_update_homestead_context():
    url = Endpoint.update_context_url
    headers = Endpoint.headers
    data = {
        "entries": [
            {
                "userQuery": ["Test Query"],
                "chatGPTResponse": ["Test Response"]
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 200

def test_add_new_entry():
    url = Endpoint.update_context_url
    headers = Endpoint.headers
    new_entry = {
        "id": str(uuid.uuid4()),
        "userQuery": ["test query"],
        "chatGPTResponse": ["test response"]
    }
    response = requests.post(url, json={"entries": [new_entry]}, headers=headers)
    assert response.status_code == 200

def test_update_existing_entry(create_entry):
    url = Endpoint.update_context_url
    headers = Endpoint.headers
    existing_entry = create_entry
    existing_id = existing_entry.id

    updated_entry = {
        "id": existing_id,
        "userQuery": ["updated query"],
        "chatGPTResponse": ["updated response"]
    }

    response = requests.post(url, json={"entries": [updated_entry]}, headers=headers)
    assert response.status_code == 200

def test_duplicate_id_handling(duplicate_entry):

    url = Endpoint.update_context_url
    headers = Endpoint.headers
    duplicate_id = duplicate_entry
    entry = {
        "id": str(duplicate_id),
        "userQuery": ["some query"],
        "chatGPTResponse": ["some response"]
    }
    response = requests.post(url, json={"entries": [entry]}, headers=headers)
    assert response.status_code == 400 

def test_id_format_validation():
    url = Endpoint.update_context_url
    headers = Endpoint.headers
    invalid_id_entry = {
        "id": "74e15761",
        "userQuery": ["test query"],
        "chatGPTResponse": ["test response"]
    }
    response = requests.post(url, json={"entries": [invalid_id_entry]}, headers=headers)
    assert response.status_code == 422

def test_delete_homestead_context(create_entry):
    existing_entry_id = create_entry 
    url = Endpoint.delete_context_url + f"deleteHHContext/{existing_entry_id}"
    headers = Endpoint.headers
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200
