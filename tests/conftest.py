import pytest
import json

from services.open_ai import Openai
from homestead.homestead import Homestead
from models.entry import RootSchema


@pytest.fixture
def openai():
    """Instance of Openai for testing."""
    _openai = Openai()

    return _openai

@pytest.fixture
def homestead():
    """Instance of Openai for testing."""
    _homestead = Homestead()

    return _homestead

@pytest.fixture
def homestead_instance(tmp_path):
    """Creates a temporary JSON file for testing then patches the Homestead class to use this temporary file."""
    temp_file = tmp_path / "test_context.json"
    with open(temp_file, 'w') as file:
        json.dump({"entries": []}, file)

    original_json = Homestead._json
    Homestead._json = str(temp_file)
    yield Homestead()
    Homestead._json = original_json

@ pytest.fixture
def entry(homestead_instance):
    user_query = ["Sample query"]
    chatGPT_response = ["Sample response"]
    new_entry = homestead_instance.create_new_entry(user_query, chatGPT_response)
    root_schema = RootSchema(entries=[new_entry])
    homestead_instance.update_homestead_context(root_schema)
    return new_entry
    return entry