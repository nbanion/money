import pytest
import pandas as pd
import pandas.testing as pdt
from .. import process as prc


@pytest.fixture
def categories():
    """Category set to use for testing."""
    return {"cat0": ["item0"]}


@pytest.fixture
def credit_bundle():
    """Raw credit card dataframe."""
    data = {
        "Transaction Date": ("01/02/2019", "01/01/2019"),
        "Post Date": ("01/03/2019", "01/02/2019"),
        "Description": ("item1", "item0"),
        "Category": ("NA", "NA"),
        "Type": ("sale", "sale"),
        "Amount": (-10, -10)
    }
    bundle = dict()
    bundle["df"] = pd.DataFrame(data)
    bundle["source"] = "credit0"
    bundle["type"] = "credit"
    bundle["edits"] = {1: "cat1"}
    return bundle


@pytest.fixture
def checking_bundle():
    """Raw chekcing dataframe."""
    data = {
        "Details": ("DEBIT", "DEBIT"),
        "Posting Date": ("01/02/2019", "01/01/2019"),
        "Description": ("item1", "item0"),
        "Amount": (-10, -10),
        "Type": ("ACH_DEBIT", "ACH_DEBIT"),
        "Balance": (100, 110),
        "Check or Slip #": (None, None)
    }
    bundle = dict()
    bundle["df"] = pd.DataFrame(data)
    bundle["source"] = "checking0"
    bundle["type"] = "checking"
    bundle["edits"] = {1: "cat1"}
    return bundle


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


def test_assemble(credit_bundle, checking_bundle,
                  categories, expected_prep_result):
    bundles = [credit_bundle, checking_bundle]
    result = prc.assemble(bundles, categories)
    expected = pd.concat([expected_prep_result, expected_prep_result],
                         keys=["credit0", "checking0"],
                         names=["source", "item"])
    pdt.assert_frame_equal(result, expected)


def test_prep_credit(credit_bundle, categories, expected_prep_result):
    df = credit_bundle["df"]
    edits = credit_bundle["edits"]
    result = prc.prep_credit(df, categories, edits=edits)
    pdt.assert_frame_equal(result, expected_prep_result)


def test_prep_checking(checking_bundle, categories, expected_prep_result):
    df = checking_bundle["df"]
    edits = checking_bundle["edits"]
    result = prc.prep_checking(df, categories, edits=edits)
    pdt.assert_frame_equal(result, expected_prep_result)


def test_get_categories():
    budget = [
        {"name": "cat0", "patterns": None},
        {"name": "cat1", "patterns": ["re0", "re1"]}
    ]
    assert prc.get_categories(budget) == {"cat1": ["re0", "re1"]}
