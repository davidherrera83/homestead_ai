import pytest

from fw import get_secret
from services.open_ai import Openai


@pytest.fixture
def secret():
    _secret_model = get_secret()

    return _secret_model


@pytest.fixture
def openai():
    _openai = Openai()

    return _openai

@pytest.fixture
def new_file():
    _file = Openai().upload_file()

    return _file
