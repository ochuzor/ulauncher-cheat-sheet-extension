import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import pytest

from grep_search_handler import SearchQueryMapper


@pytest.fixture
def query_mapper_sut():
    ''' Returns a basic search query mapper '''
    return SearchQueryMapper()


def test_empty_string_mapping(query_mapper_sut):
    assert query_mapper_sut.map('') == {"dest": "", "term": ""}
    assert query_mapper_sut.map(' ') == {"dest": "", "term": ""}
    assert query_mapper_sut.map('     ') == {"dest": "", "term": ""}
    assert query_mapper_sut.map('  \t   ') == {"dest": "", "term": ""}


def test_str_with_src_query(query_mapper_sut):
    assert query_mapper_sut.map('#') == {"dest": "", "term": ""}
    assert query_mapper_sut.map('vim #') == {"dest": "", "term": "vim #"}
    assert query_mapper_sut.map('vim # search term') == {"dest": "", "term": "vim # search term"}
    assert query_mapper_sut.map('  #   \t ') == {"dest": "", "term": ""}
    assert query_mapper_sut.map('#vim') == {"dest": "vim", "term": ""}
    assert query_mapper_sut.map('#vim search term') == {"dest": "vim", "term": "search term"}
    assert query_mapper_sut.map('# vim') == {"dest": "", "term": "vim"}
    assert query_mapper_sut.map('# vim search term') == {"dest": "", "term": "vim search term"}
    assert query_mapper_sut.map('   #vim     \t ') == {"dest": "vim", "term": ""}
    assert query_mapper_sut.map('   #vim     \t go to file') == {"dest": "vim", "term": "go to file"}
