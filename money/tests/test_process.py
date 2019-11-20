import pytest
from .. import process


def test_categories():
    budget = [
        {"name": "cat0", "patterns": None},
        {"name": "cat1", "patterns": ["re0", "re1"]}
    ]
    assert process.categories(budget) == {"cat1": ["re0", "re1"]}
