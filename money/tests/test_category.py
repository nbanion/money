import pytest
from .. import category


def test_list_candidates():
    string = "COFFEE 001"
    categories = {"coffee": [r"COFFEE \d+"], "groceries": ["blah"]}
    assert category.list_candidates(string, categories) == ["coffee"]


def test_is_match():
    string = "COFFEE 001"
    patterns0 = ["blah"]
    patterns1 = ["blah", r"COFFEE \d+"]
    assert category.is_match(string, patterns0) == False
    assert category.is_match(string, patterns1) == True
