import os.path
import requests

from os import path
from fw import get_token

herrera_homestead_file = 'hh_context.json'

def test_json_file_exists():
    assert path.exists(herrera_homestead_file)

def test_json_file_not_empty():
    assert os.stat(herrera_homestead_file).st_size is not 0

def test_get_homestead_context():
    url = "http://localhost:8000/getHHContext"
    headers = {"Token": f"Bearer {get_token().token}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200

def test_update_homestead_context():
    url = "http://localhost:8000/updateHHContext"
    headers = {"Token": f"Bearer {get_token().token}"}
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