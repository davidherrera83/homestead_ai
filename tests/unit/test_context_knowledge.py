import os.path
from os import path

herrera_homestead_file = 'hh_context.md'

def test_md_file_exists():
    assert path.exists(herrera_homestead_file)

def test_md_file_not_empty():
    assert os.stat(herrera_homestead_file).st_size is not 0