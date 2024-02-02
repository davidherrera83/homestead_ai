import os
import json

from os import path
from unittest.mock import patch

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


def test_delete_context_by_id(entry, homestead):
    entry_id = f"{entry.id}"

    with open(homestead._json, 'r') as file:
        data = json.load(file)
        assert any(entry['id'] == entry_id for entry in data['entries'])

    homestead.delete_entry_by_id(entry_id)

    with open(homestead._json, 'r') as file:
        data = json.load(file)
        assert not any(entry['id'] == entry_id for entry in data['entries'])

@patch('homestead.homestead.Homestead.conversation')
def test_homestead_workflow(mock_conversation, openai, homestead_instance):
    mock_initial_response = [{"role": "assistant", "content": [{"type": "text", "text": {"value": "Mocked initial response"}}]}]
    mock_continued_response = [{"role": "assistant", "content": [{"type": "text", "text": {"value": "Mocked continued response"}}]}]
    mock_conversation.side_effect = [
        (mock_initial_response, "mock_thread_id"),
        (mock_continued_response, "mock_thread_id")
    ]

    # Initial Query
    user_query = "Now that I have completed the AI assistant from Open AI, How can I interact with it using a GUI?"
    initial_response, thread_id = homestead_instance.conversation(user_query)
    initial_assistant_response = homestead_instance.process_response_and_update_context(user_query, initial_response, thread_id)
    assert initial_assistant_response is not None, "Initial response parsing failed"

    # Continued Conversation
    user_reply = "Can you create a software roadmap for that?"
    continued_response, thread_id = homestead_instance.conversation(user_reply, thread_id)
    continued_assistant_response = homestead_instance.process_response_and_update_context(user_reply, continued_response, thread_id)

    assert continued_assistant_response is not None, "Continued response parsing failed"
