import pytest
import pandas as pd
import pandas.testing as pdt
from .. import process as prc


@pytest.fixture
def raw_credit():
    """Raw credit card dataframe."""
    data_df = {
        "Transaction Date": ("01/02/2019", "01/01/2019"),
        "Post Date": ("01/03/2019", "01/02/2019"),
        "Description": ("item1", "item0"),
        "Category": ("NA", "NA"),
        "Type": ("sale", "sale"),
        "Amount": (-10, -10)
    }
    return pd.DataFrame(data_df)


@pytest.fixture
def raw_checking():
    """Raw chekcing dataframe."""
    data_df = {
        "Details": ("DEBIT", "DEBIT"),
        "Posting Date": ("01/02/2019", "01/01/2019"),
        "Description": ("item1", "item0"),
        "Amount": (-10, -10),
        "Type": ("ACH_DEBIT", "ACH_DEBIT"),
        "Balance": (100, 110),
        "Check or Slip #": (None, None)
    }
    return pd.DataFrame(data_df)


@pytest.fixture
def expected_prep_result():
    """Expected dataframe after preparing credit or checking data."""
    data = {
        "date": pd.Series(("01/01/2019", "01/02/2019"), dtype="datetime64[ns]"),
        "desc": ("item0", "item1"),
        "amount": (-10, -10),
        "category": ("cat0", "cat1")
    }
    return pd.DataFrame(data)[::-1]


def test_assemble(raw_credit, raw_checking, expected_prep_result):
    bundles = [
        {"df": raw_credit, "source": "s0", "type": "credit", "edits": {1: "cat1"}},
        {"df": raw_checking, "source": "s1", "type": "checking", "edits": {1: "cat1"}},
    ]
    categories = {"cat0": ["item0"]}
    result = prc.assemble(bundles, categories)
    expected = pd.concat([expected_prep_result, expected_prep_result],
                         keys=["s0", "s1"], names=["source", "item"])
    pdt.assert_frame_equal(result, expected)


def test_prep_credit(raw_credit, expected_prep_result):
    categories = {"cat0": ["item0"]}
    edits = {1: "cat1"}
    result = prc.prep_credit(raw_credit, categories, edits=edits)
    pdt.assert_frame_equal(result, expected_prep_result)


def test_prep_checking(raw_checking, expected_prep_result):
    categories = {"cat0": ["item0"]}
    edits = {1: "cat1"}
    result = prc.prep_checking(raw_checking, categories, edits=edits)
    pdt.assert_frame_equal(result, expected_prep_result)


def test_categories():
    budget = [
        {"name": "cat0", "patterns": None},
        {"name": "cat1", "patterns": ["re0", "re1"]}
    ]
    assert prc.categories(budget) == {"cat1": ["re0", "re1"]}
