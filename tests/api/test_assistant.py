import os
import json
import pytest

from os import path
from models.entry import EntryModel, RootSchema
from fw import Files



def test_json_file_exists():
    herrera_homestead_file = 'hh_context.json'
    assert path.exists(herrera_homestead_file)


def test_json_file_not_empty():
    herrera_homestead_file = 'hh_context.json'
    assert os.stat(herrera_homestead_file).st_size is not 0


def test_create_new_entry_in_context(homestead_instance):
    user_query = ["Sample query"]
    chatGPT_response = ["Sample response"]
    entry = homestead_instance.create_new_entry(user_query, chatGPT_response)
    assert entry.userQuery == user_query
    assert entry.chatGPTResponse == chatGPT_response


def test_add_assistant_response_to_context_file(openai, homestead):
    user_query = "What is the PP part of HH?"
    response = openai.homestead(user_query)
    assistant_response = openai.parse_response(user_query, response)

    if assistant_response:
        entry = EntryModel(**assistant_response)
        root_schema = RootSchema(entries=[entry])
        homestead.update_homestead_context(root_schema)
    else:
        assert assistant_response is not None, "Failed to parse response"

@pytest.mark.parametrize(
        "entry_id",[
            "80c5950f-53a5-4840-9dce-43a0a6cbe382"
        ]
)
def test_delete_context_by_id(entry_id, homestead):
    entry_id = f"{entry_id}"

    with open(homestead._json, 'r') as file:
        data = json.load(file)
        assert any(entry['id'] == entry_id for entry in data['entries'])

    homestead.delete_entry_by_id(entry_id)

    with open(homestead._json, 'r') as file:
        data = json.load(file)
        assert not any(entry['id'] == entry_id for entry in data['entries'])

def test_homestead_workflow(openai, homestead):
    user_query = "What would be the best strategy to advertise the Mentoring service of HH?"
    response = openai.homestead(user_query)
    assistant_response = homestead.parse_response(user_query, response)
    if assistant_response:
        entry = EntryModel(**assistant_response)
        root_schema = RootSchema(entries=[entry])
        homestead.update_homestead_context(root_schema)
        old_file_id = Files.file_id
        new_file_id = openai.upload_files()
        openai.delete_file(old_file_id)
        homestead.update_file_id_in_secrets(new_file_id)
    else:
        assert assistant_response is not None, "Failed to parse response"
