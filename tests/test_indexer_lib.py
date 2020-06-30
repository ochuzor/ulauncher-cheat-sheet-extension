import pytest

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from src.indexer_lib import get_tokens, get_ngrams, get_normalized_string, get_string_chunks

def test_get_tokens():
    assert get_tokens('') == []
    assert get_tokens('one') == ['one']
    assert get_tokens('Take that!') == ['take', 'that', 'take that']


def test_get_ngrams_empty_string():
    assert get_ngrams('', 1) == []


def test_get_ngrams_of_size_1():
    assert get_ngrams('', 1) == []
    assert get_ngrams('one', 1) == ['one']
    assert get_ngrams('find file', 1) == ['find', 'file']
    assert get_ngrams('we got it', 1) == ['we', 'got', 'it']
    assert get_ngrams('where is the money', 1) == ['where', 'is', 'the', 'money']
    assert get_ngrams('from the chap who left before the party started', 1) == ['from', 'the', 'chap', 'who', 'left', 'before', 'the', 'party', 'started']


def test_get_ngrams_of_size_2():
    assert get_ngrams('', 2) == []
    assert get_ngrams('one', 2) == ['one']
    assert get_ngrams('find file', 2) == ['find file']
    assert get_ngrams('we got it', 2) == ['we got', 'got it']
    assert get_ngrams('where is the money', 2) == ['where is', 'is the', 'the money']
    assert get_ngrams('from the chap who left before the party started', 2) == [
            'from the', 'the chap', 'chap who', 'who left', 'left before', 'before the',
            'the party', 'party started'
        ]


def test_get_normalized_string():
    assert get_normalized_string('') == ''
    assert get_normalized_string('where     is       it') == 'where is it'
    assert get_normalized_string("Well,     THat's   just Great!") == "well thats just great"


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
    assert get_string_chunks('one! He yelled') == ['one', 'he yelled']
    assert get_string_chunks('one! ! He yelled') == ['one', 'he yelled']