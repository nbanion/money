"""Utilities for categorizing transactions.

This module provides functionality for categorizing series__ of transactions
using regex-based categorization schemes and index-specific manual edits. It is
useful for categorizing transactions and for validating categorizations.

__ https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html

The module has the following high-level functions. These functions take series
and categorization instructions, and they return new series.

- :func:`money.category.categorize` applies a category to each item.
- :func:`money.category.count_candidates` counts candidate categories by item.

These high-level functions take a series of transaction descriptions, and they
use these transaction descriptions and their indices to assign categories.

The functions use two other inputs to assign cateogies. The first is a dict of
catergories. The keys in this dict are categories, and the values are lists of
regular expressions. If a description fully matches any of the regular
expressions, then it fits the category. An example category dict: ::

    {"cat0": ["re0", ...], ...}

The second input is a dict of index-specific manual edits. The keys in this dict
are indices, and the values are categories to assign. For example: ::

    {0: "cat0", ...}

In this example, we start by defining a series, categories, and edits. ::

    import pandas as pd
    import category

    # Series of descriptions. Changing the index for demonstration.
    series = pd.Series(["blah", "COFFEE 001", "stuff"],
                       index=[10, 11, 12])

    # Categories with regular expressions.
    categories = {"coffee": [r"COFFEE \\d+"]}

    # Index-specific manual categorizations.
    edits = {11: "misc", 12: "misc"}

Next, we apply categories to the series. Note how the second transaction
description is recognized as coffee, and the third transaction is hard coded as
miscellaneous. As the second transaction shows, the algorithm favors regex
matches over hard codes. ::

    category.categorize(series, categories, edits=edits)
    # 10      None
    # 11    coffee
    # 12      misc

Ideally, the algorithm shouldn't have to make a choice; each transaction should
have one and only one category. When we test this condition, we can see that
the first transaction has no categories, and the second transaction has two
categories. We might want to address these cases before analysis. ::

    category.count_candidates(series, categories, edits=edits)
    # 10    0
    # 11    2
    # 12    1

Each high-level function has a companion ``row_*`` function that applies an
algorithm to each value in the series.
:func:`money.category.row_list_candidates` does most of the categorizing work.

The high-level functions use :func:`money.category.apply_to_series_using_index`
to apply the ``row_*`` functions in a way that exposes the series index.

"""
import pandas as pd
import re


def categorize(series, categories, edits=None):
    """Assign categories for a series of transaction descriptions.

    This function applies :func:`money.category.row_categorize` to every value
    in a ``series``, creating a series of categories with the same index.

    Arguments:
        series: Length 2 iterable of transaction descriptions.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        A Pandas Series with categories.

    """
    return apply_to_series_using_index(row_categorize, series,
                                       categories, edits=edits)


def count_candidates(series, categories, edits=None):
    """Count candidate categories for a series of transaction descriptions.

    This function applies :func:`money.category.row_count_candidates` to every
    value in a ``series``, creating a series of counts with the same index.

    Arguments:
        series: Length 2 iterable of transaction descriptions.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        A Pandas Series with counts.

    """
    return apply_to_series_using_index(row_count_candidates,
                                       series, categories, edits=edits)


def row_categorize(row, categories, edits=None):
    """Categorize one indexed transaction "row".

    The function arbitrarily returns the first candidate category assigned to
    the row. It's written with the expectation that each row *should* only fit
    one category. In practice, it's a good idea to test this assumption.

    Arguments:
        row: Length 2 iterable with an index and a description.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        str: A category for the row.

    """
    candidates = row_list_candidates(row, categories, edits=edits)
    if candidates:
        return candidates[0]


def row_count_candidates(row, categories, edits=None):
    """Count candidate categories for one indexed transaction "row".

    Arguments:
        row: Length 2 iterable with an index and a description.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        int: Number of candidate categoires for the row.

    """
    candidates = row_list_candidates(row, categories, edits=edits)
    return len(candidates)


def row_list_candidates(row, categories, edits=None):
    """Identify candidate categories for one indexed transaction "row".

    Each row has two fields. The first is the transaction index, and the second
    is the transaction description. This function uses the index to assign
    manual category edits to specific transactions.

    Arguments:
        row: Length 2 iterable with an index and a description.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        list: Candidate categories for the row.

    """
    index, description = row
    candidates = []
    # Pattern match descriptions to categories.
    for category, patterns in categories.items():
        if is_match(description, patterns):
            candidates.append(category)
    # Apply index-specific manual categorizations.
    if edits:
        category = edits.get(index)
        if category:
            candidates.append(category)
    return candidates


def apply_to_series_using_index(f, series, *args, **kwargs):
    """Apply a function to a series, making the series index available.

    The function converts the ``series`` to a two-column data frame with the
    series index as a column, so that function ``f`` can process the index when
    doing its job. Afterward, the data frame returns to a series with the
    original index intact. See `Stack Overflow`__.

    __ https://stackoverflow.com/a/18316830

    This function could be written as a wrapper for ``f``, but it becomes
    unclear while glancing at the arguments of ``f`` whether it should take a
    series or a row as its first argument. The current approach is transparent.

    Arguments:
        f (function): Function to apply to the series.
        series: Pandas Series to have the function applied.
        *args: Additional positional argmunents for ``f``.
        **kwargs: Additional keyword arguments for ``f``.

    Returns:
        A Pandas series with the function applied.

    """
    result = (series.reset_index()
                    .apply(f, axis=1, args=args, **kwargs))
    return pd.Series(result.values, index=series.index)


def is_match(string, patterns):
    """Test if a string matches any pattern in a given list.

    Arguments:
        string (str): String that might match ``patterns``.
        patterns (list): Patterns to match.

    Returns:
        bool: True for a match, otherwise false.

    """
    return any([re.fullmatch(p, string) for p in patterns])
