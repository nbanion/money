Source Data
===========

This project uses three data sources:

- **Budget Items:** Planned income and expenses.
- **Transactions:** Bank data on individual units of income and expenses.
- **Metadata:** Additional information about transactions.


Budget Items
------------

Budget items represent categories of planned income and expenses. A set of
budget items should cover all transactions in a year, using catch-all categories
as needed. A budget is a list of budget items. For example:

.. code-block:: yaml

  - name: income   # Description of the budget item.
    type: annual   # How often the transaction occurs.
    amount: 1000   # Value in dollars (positive or negative).
    weekly: false  # Include in the weekly budget report?
  ...

We define budget items in YAML format and store them in ``data/budgets``.


Transactions
------------

Transactions represent individual units of income and expenses. Transactions
come from credit card and checking accounts. The data from these different
sources have slightly different fields, but the most of the same basic
information. The credit card transaction fields are:

- **Transaction Date:** Date the transaction occurred.
- **Post Date:** Date the transaction was posted to the account.
- **Description:** Description of the transaction.
- **Category:** Bank-defined category of the transaction.
- **Type:** Transaction type?
- **Amount:** Value in dollars (positive or negative).

The checking account transaction fields are:

- **Details:** Details about the transaction?
- **Posting Date:** Date the transaction was posted to the account.
- **Description:** Description of the transaction.
- **Amount:** Value in dollars (positive or negative).
- **Type:** Transaction type?
- **Balance:** Remaining balance after the transaction.
- **Check or Slip #:** Number on the check, where applicable.

We download weekly transaction CSVs from the bank and store them in
``data/transactions``.


Metadata
--------

Transactions require some processing before analysis. Rather than modifying the
raw transaction data directly, we generate metadata that we can append to the
transaction data.

The metadata allow us to re-categorize transactions to conform to budget
categories. We can categorize many transactions using rules (e.g., by
identifying keywords in descriptions), but other transactions require human
review. These metadata ensure that the human judgment calls are preserved.

This re-categorization is especially important for removing credit card payments
from checking transaction history. We already record credit card transactions
for specific purchases, and recording credit card payments would cause us to
double count these transactions.

**We are able to leave out credit card payments and count the individual
transactions only because we autopay the credit card bill and keep no credit
card debt.** If these circumstances change, then we will have to reevaluate this
accounting approach.

Each case in the metadata corresponds to a transaction. The metadata include the
following fields:

- **dataset:** The dataset where the transaction can be found.
- **row:** The row of the transaction within the dataset.
- **category:** A category that corresponds to the budget categories.

We generate metadata CSVs and store them in ``data/metadata``.

.. note::

  Develop a tool that helps with generating metadata.


.. develop a tool. lags.
