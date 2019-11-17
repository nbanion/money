"""Utilities for categorizing transactions.
"""
import re


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
