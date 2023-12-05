import json
import os

from models.token import TokenModel

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_token() -> TokenModel:
    """
    Get the TokenModel from secrets.json
    """
    with open(_ROOT_DIR + '/secrets.json', 'r') as json_file:
        _json = json.loads(json_file.read())

        return TokenModel(**_json)
