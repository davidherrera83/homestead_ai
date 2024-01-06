import pytest

from services.open_ai import Openai
from datetime import datetime
from fw import get_token


def test_homestead_io(token):
    response = Openai(token).homestead("What are the states with no income tax?")
    assert response.status_code == 200
