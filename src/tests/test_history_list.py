import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import pytest

from grep_search_handler import HistoryList


@pytest.fixture
def history_list_sut():
    ''' Returns a basic history list object '''
    return HistoryList(result_list = [], max_items_count = 3)


def test_add_duplicate(history_list_sut):
    history_list_sut.add({"id": 1})
    ls_1 = history_list_sut.to_list()
    assert len(ls_1) == 1

    history_list_sut.add({"id": 1})
    ls_2 = history_list_sut.to_list()
    assert len(ls_2) == 1
    assert ls_1 == ls_2


def test_add_more_items(history_list_sut):
    history_list_sut.add({"id": 1})
    history_list_sut.add({"id": 2})
    history_list_sut.add({"id": 3})
    assert history_list_sut.to_list() == [{"id": 3}, {"id": 2}, {"id": 1}]

    history_list_sut.add({"id": 4})
    assert history_list_sut.to_list() == [{"id": 4}, {"id": 3}, {"id": 2}]
