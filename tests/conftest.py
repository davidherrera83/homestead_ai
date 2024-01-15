import pytest

from fw import get_token
from services.open_ai import Openai


@pytest.fixture
def token():
    _token_model = get_token()

    return _token_model


@pytest.fixture
def openai():
    _openai = Openai()

    return _openai

@pytest.fixture
def new_file():
    _file = Openai().upload_file()

    return _file
