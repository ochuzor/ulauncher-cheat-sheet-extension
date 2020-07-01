import pytest

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from src.indexer_lib import get_tokens, get_digrams, get_normalized_string, get_string_chunks

def test_get_tokens():
    assert get_tokens('') == []
    assert get_tokens('one') == ['one']
    assert get_tokens('Take that!') == ['take', 'that', 'take that']
    assert get_tokens("Need for speed. I'm trynna take the lead.") == [
        "need", "for", "speed", "need for", "for speed", "im", "trynna", "take",
        "the", "lead", "im trynna", "trynna take", "take the", "the lead"
    ]


def assert_list_h(list_1, list_2):
    return len(list_1) == len(list_2) and set(list_1) == set(list_2)


def test_assert_list_h():
    assert assert_list_h(['one', 'two', 'three'], ['two', 'one', 'three']) == True
    assert assert_list_h(['one', 'two'], ['two', 'one', 'three']) == False
    assert assert_list_h(['one', 'one'], ['one', 'two']) == False
    assert assert_list_h(['one', 'one'], ['two', 'one']) == False
    assert assert_list_h(['one', 'two'], ['one', 'two']) == True


def test_get_digrams():
    assert get_digrams([]) == []
    assert get_digrams(['one']) == []
    assert get_digrams(['find', 'file']) == ['find file']
    assert assert_list_h(get_digrams(['we', 'got', 'it']), ['we got', 'got it']) == True

    assert assert_list_h(get_digrams(['where', 'is', 'the', 'money']), 
        ['where is', 'is the', 'the money']) == True

    digrams = get_digrams(['from', 'the', 'chap', 'who', 'left', 'before', 'the', 'party', 'started'])
    expected_digrams = [ 'from the', 'the chap', 'chap who', 'who left', 'left before', 
    'before the', 'the party', 'party started']
    assert assert_list_h(digrams, expected_digrams) == True


def test_get_normalized_string():
    assert get_normalized_string('') == ''
    assert get_normalized_string('where     is       it') == 'where is it'
    assert get_normalized_string("Well,     THat's   just Great!") == "well that's just great"
    assert get_normalized_string("@money! It's all #* #num") == "money it all about num"


def test_get_string_chunks():
    assert get_string_chunks('') == []
    assert get_string_chunks('one') == ['one']
    assert get_string_chunks('one!') == ['one']
    assert get_string_chunks('What is that?') == ['What is that']
    assert get_string_chunks('Where is it? Did you take it?') == ['Where is it', 'Did you take it']
    assert get_string_chunks('I got one, two, three') == ['I got one', 'two', 'three']
    assert get_string_chunks('I have one goal: to find her.') == ['I have one goal', 'to find her']
    assert get_string_chunks('Call me tomorrow; you can give me an answer then.') == ['Call me tomorrow', 'you can give me an answer then']
    assert get_string_chunks('Bring any two items; however, sleeping bags and tents are in short supply.   ') == [
        'Bring any two items', 'however', 'sleeping bags and tents are in short supply']
    assert get_string_chunks('one! He yelled') == ['one', 'He yelled']
    assert get_string_chunks('one! ! He yelled') == ['one', 'He yelled']