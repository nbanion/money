import pytest
import pandas as pd
import pandas.testing as pdt
from .. import process


@pytest.fixture
def expected_prep_result():
    """Expected dataframe after preparing credit or checking data."""
    data = {
        "date": pd.Series(("01/01/2019", "01/02/2019"), dtype="datetime64[ns]"),
        "desc": ("item0", "item1"),
        "amount": (-10, -10),
        "source": ("test", "test"),
        "category": ("cat0", "cat1")
    }
    return pd.DataFrame(data)[::-1]


def test_prep_credit(expected_prep_result):
    categories = {"cat0": ["item0"]}
    edits = {1: "cat1"}
    data_df = {
        "Transaction Date": ("01/02/2019", "01/01/2019"),
        "Post Date": ("01/03/2019", "01/02/2019"),
        "Description": ("item1", "item0"),
        "Category": ("NA", "NA"),
        "Type": ("sale", "sale"),
        "Amount": (-10, -10)
    }
    df = pd.DataFrame(data_df)
    result = process.prep_credit(df, categories, edits=edits, source="test")
    pdt.assert_frame_equal(result, expected_prep_result)


def test_prep_checking(expected_prep_result):
    categories = {"cat0": ["item0"]}
    edits = {1: "cat1"}
    data_df = {
        "Details": ("DEBIT", "DEBIT"),
        "Posting Date": ("01/02/2019", "01/01/2019"),
        "Description": ("item1", "item0"),
        "Amount": (-10, -10),
        "Type": ("ACH_DEBIT", "ACH_DEBIT"),
        "Balance": (100, 110),
        "Check or Slip #": (None, None)
    }
    df = pd.DataFrame(data_df)
    result = process.prep_checking(df, categories, edits=edits, source="test")
    pdt.assert_frame_equal(result, expected_prep_result)


def test_categories():
    budget = [
        {"name": "cat0", "patterns": None},
        {"name": "cat1", "patterns": ["re0", "re1"]}
    ]
    assert process.categories(budget) == {"cat1": ["re0", "re1"]}
