import pytest
import pandas as pd
from .. import category


def test_categorize():
    """Tests category.categorize.

    Tests that:
    - Function returns a series.
    - Result has categories from ``categories`` and ``edits``.
    - Result preserves the input series index.

    """
    series = pd.Series(["blah", "COFFEE 001", "stuff"], index=[10, 11, 12])
    categories = {"coffee": [r"COFFEE \d+"]}
    edits = {12: "misc"}
    result = category.categorize(series, categories, edits=edits)
    assert type(result) == pd.Series
    assert result.to_list() == [None, "coffee", "misc"]
    assert result.index.to_list() == [10, 11, 12]


def test_row_categorize():
    row = pd.Series([1, "COFFEE 001"])
    categories = {"coffee": [r"COFFEE \d+"]}
    edits = {1: "misc"}
    result = category.row_categorize(row, categories, edits=edits)
    assert result == "coffee"


def test_row_list_candidates():
    row = pd.Series([1, "COFFEE 001"])
    categories = {"coffee": [r"COFFEE \d+"]}
    edits = {1: "misc"}
    result = category.row_list_candidates(row, categories, edits=edits)
    assert result == ["coffee", "misc"]


def test_is_match():
    string = "COFFEE 001"
    patterns0 = ["blah"]
    patterns1 = ["blah", r"COFFEE \d+"]
    assert category.is_match(string, patterns0) == False
    assert category.is_match(string, patterns1) == True
