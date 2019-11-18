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

    This function applies :func:`category.row_categorize` to every value
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

    This function applies :func:`category.row_count_candidates` to every value
    in a ``series``, creating a series of counts with the same index.

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


def is_match(string, patterns):
    """Test if a string matches any pattern in a given list.

    Arguments:
        string (str): String that might match ``patterns``.
        patterns (list): Patterns to match.

    Returns:
        bool: True for a match, otherwise false.

    """
    return any([re.fullmatch(p, string) for p in patterns])
