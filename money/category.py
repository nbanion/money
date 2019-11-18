"""Utilities for categorizing transactions.
"""
import pandas as pd
import re


def apply_to_series_using_index(f, series, *args, **kwargs):
    """Apply a function to a series, make the series index available.

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


def categorize(series, categories, edits=None):
    """Assign categories for a series of transaction descriptions.

    This function applies :func:`category.categorize_row` to every value
    in a ``series``, creating a series of categories with the same index.

    Arguments:
        series: Pandas Series of transaction descriptions.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        A Pandas Series with categories.

    """
    return apply_to_series_using_index(categorize_row, series,
                                       categories, edits=edits)


def categorize_row(row, categories, edits=None):
    """Categorize one indexed transaction "row".

    Each row has two fields. The first is the transaction index, and the second
    is the transaction description. This function uses the index to assign
    manual category edits to specific transactions.

    The function arbitrarily returns the first candidate category assigned to
    the row. It's written with the expectation that each row *should* only fit
    one category.

    Arguments:
        row: Pandas Series with an index and a description.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        str: A category for the row.

    """
    index, description = row
    candidates = list_candidates(description, categories)
    if edits:
        category = edits.get(index)
        if category:
            candidates.append(category)
    if candidates:
        return candidates[0]


def list_candidates(string, categories):
    """Find candidate categories for a string.

    If ``string`` matches any of the regular expressions associated with a
    category from ``categories``, then this function includes that category as a
    candidate category for the string.

    Arguments:
        string (str): String to categorize.
        categories (dict): Regex patterns for each category. ::

            {"cat0": ["re0", ...] ...}

    Returns:
        list: Candidate categories for the string. ::

            ["cat0", ...]

    """
    candidates = []
    for category, patterns in categories.items():
        if is_match(string, patterns):
            candidates.append(category)
    return candidates


def is_match(string, patterns):
    """Test if a string matches any pattern in a given list.

    Arguments:
        string (str): String that might match ``patterns``.
        patterns (list): Patterns to match.

    Returns:
        bool: True for a match, otherwise false.

    """
    return any([re.fullmatch(p, string) for p in patterns])
