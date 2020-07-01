import pytest

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from src.lib import get_search_object

def test_get_search_object_empty_string():
    assert get_search_object('') == {'filter_str': '', 'search_string': ''}