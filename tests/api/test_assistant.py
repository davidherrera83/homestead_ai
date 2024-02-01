import os
import json
import pytest

from os import path
from models.entry import EntryModel, RootSchema
from fw import Files, get_secret as secrets



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
    

@pytest.mark.parametrize(
        "entry_id",[
            "7ec50aaf-a653-439e-91c4-be779fc5ff5f"
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
    user_query = "How can completing my AI assistant from OpenAI help the furniture flipping business of HH?"
    response, thread_id = homestead.conversation(user_query)
    assistant_response = homestead.parse_response(user_query, response, thread_id)
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

def test_reply_to_homestead(openai, homestead):
    # Initial Query
    user_query = "Now that I have completed the AI assistant, can I create a chatbot for my Macbook?"
    initial_response, thread_id = homestead.conversation(user_query)
    initial_assistant_response = homestead.parse_response(user_query, initial_response, thread_id)

    # Update Homestead context after initial response
    if initial_assistant_response:
        entry = EntryModel(**initial_assistant_response)
        root_schema = RootSchema(entries=[entry])
        homestead.update_homestead_context(root_schema)

    # Assertions for initial response
    assert 'thread_id' in initial_assistant_response, "Thread ID missing in initial response"

    # Continued Conversation
    user_reply = "Can you create a software roadmap for that?"
    continued_response, thread_id = homestead.conversation(user_reply, thread_id)

    continued_assistant_response = homestead.parse_response(user_reply, continued_response, thread_id)

    # Update Homestead context after continued response
    if continued_assistant_response:
        entry = EntryModel(**continued_assistant_response)
        root_schema = RootSchema(entries=[entry])
        homestead.update_homestead_context(root_schema)

        # Manage files
        old_file_id = Files.file_id
        new_file_id = openai.upload_files()
        openai.delete_file(old_file_id)
        homestead.update_file_id_in_secrets(new_file_id)
    else:
        assert continued_assistant_response is not None, "Failed to parse continued response"

    # Assertions for continued response
    assert continued_assistant_response is not None, "Continued response parsing failed"
