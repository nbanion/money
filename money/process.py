"""Utilities for processing raw data.

Notes:

- Top level functions.
- Usage and example.
- Describe need to harmonize credit and checking data.
- Document and link to commonly used special data structures.
    - Budget / categories.
    - Edits.
    - Processing configurations.

"""
import pandas as pd
from . import category as cg


def process(credit_paths, checking_paths, budget_path):
    """Process raw transaction data.

    Arguments:
        credit_paths (list): Length 2 iterables, each with paths to a credit
            card transaction CSV and a file with manual edits for the CSV.
        checking_paths (list): Length 2 iterables, each with paths to a checking
            transaction CSV and a file with manual edits for the CSV.
        budget_path (str): Path to a budget file.

    Returns:
        A Pandas dataframe with processed transaction data.

    """
    pass


def assemble(bundles, categories):
    """Prepare and combine credit and checking transactions.

    Each of the ``bundles`` is a dict representing a source
    dataframe. Each dict contains the dataframe, the data source, the prep
    method type to use, and any individual edits to apply. ::

        {
            "df": pd.DataFrame(...),
            "source": "credit000.csv"
            "type": "credit",
            "edits": {1: "cat1", ...}
        }

    This function stacks the input dataframes and assigns a two-level index to
    the result, with cases grouped by source and by the source data indices.

    Arguments:
        bundles (list): Dicts representing source datasets.
        categories (dict): Regex patterns for each category.

    """
    prep_functions = {
        "credit": prep_credit,
        "checking": prep_checking
    }

    frames = []
    for b in bundles:
        prep_function = prep_functions[b["type"]]
        prepped = (b["df"].pipe(prep_function, categories, edits=b["edits"]))
        frames.append(prepped)

    keys = [b["source"] for b in bundles]
    return pd.concat(frames, keys=keys, names=["source", "item"])


def prep_credit(df, categories, edits=None):
    """Prepare credit card transaction data for processing.

    The input dataset includes columns "Transaction Date" and "Post Date". The
    first of these columns is the date that a transaction occurred. The second
    is the date that a transaction was processed and posted to the transaction
    history. This function uses the transaction date.

    Arguments:
        df : Pandas dataframe with transaction data.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        A Pandas dataframe of prepped data.

    """
    cols = {
        "date": "Transaction Date",
        "desc": "Description",
        "amount": "Amount"
    }
    return prep_transactions(df, cols, categories, edits=edits)


def prep_checking(df, categories, edits=None):
    """Prepare checking transaction data for processing.

    Arguments:
        df : Pandas dataframe with transaction data.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        A Pandas dataframe of prepped data.

    """
    cols = {
        "date": "Posting Date",
        "desc": "Description",
        "amount": "Amount"
    }
    return prep_transactions(df, cols, categories, edits=edits)


def prep_transactions(df, cols, categories, edits=None):
    """Prepare transaction data for processing.

    This function performs the following transformations:

    - Subset columns to transaction dates, descriptions, and amounts.
    - Rename columns with shorter, standardized names.
    - Reverse the index to start with the earliest transaction.
    - Update variable ``date`` to have the datetime dtype.
    - Add variable ``category`` to categorize the transaction.

    Argument ``cols`` is a dict with the following keys:

    - ``date``: The date of the transaction.
    - ``desc``: The transaction description.
    - ``amount``: The transaction dollar amount.

    The values for this dict are the names of the columns that have these values
    in the input dataframe.

    The function reverses the index so that transactions keep the same indices
    as the input ``df`` grows. The transaction source data are cumulative
    datasets, and new cases appear at the top (index 0), changing the indices
    for all transactions in the data. Reversing the index makes sure that all
    transactions have constant indicies that correspond to transaction order.

    Arguments:
        df : Pandas dataframe with transaction data.
        cols (dict): Columns to process from the source ``df``.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        A Pandas dataframe of prepped transaction data.

    """
    colnames = ["date", "desc", "amount"]
    keeps = [cols[c] for c in colnames]
    renames = {cols[c]: c for c in colnames}
    return (df.loc[:, keeps]
              .rename(columns=renames)
              .set_index(df.index[::-1])  # Reverse index.
              .assign(date=lambda x: pd.to_datetime(x["date"]))
              .assign(category=lambda x: cg.categorize(x["desc"],
                                                       categories,
                                                       edits=edits)))


def categories(budget):
    """Extract a category dict from a budget.

    Arguments:
        budget (list): List of budget items.

    Returns:
        A dict of categories.

    """
    categories = dict()
    for item in budget:
        if item["patterns"]:
            categories[item["name"]] = item["patterns"]
    return categories
