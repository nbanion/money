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


def prep_credit(df, categories, edits=None):
    """Prepare credit card transaction data for processing.

    Arguments:
        df (str): Pandas dataframe with transaction data.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        A Pandas dataframe of prepped credit card data.

    """
    pass


def prep_checking(df, categories, edits=None):
    """Prepare checking transaction data for processing.

    Arguments:
        df (str): Pandas dataframe with transaction data.
        categories (dict): Regex patterns for each category.
        edits (dict): Index-specific manual categorizations.

    Returns:
        A Pandas dataframe of prepped checking data.

    """
    pass


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
