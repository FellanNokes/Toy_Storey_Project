import pytest

from products import get_products
from sales import generate_month

YEAR = 2025
MONTH = 3


@pytest.fixture(scope="module")
def transactions() -> list[dict]:
    """One month of generated transactions, shared by all tests in this file."""
    return generate_month(get_products(), YEAR, MONTH)


def test_transaction_id_is_unique_within_month(transactions):
    ids = [t["transaction_id"] for t in transactions]
    assert len(ids) == len(set(ids))

def test_total_amount_equals_sum_of_line_totals(transactions):
    for t in transactions:
        line_sum = sum(item["line_total"] for item in t["items"])
        assert t["total_amount"] == pytest.approx(line_sum, abs=0.01), t["transaction_id"]

def test_returns_have_negative_amounts(transactions):
    returns = [t for t in transactions if t["transaction_type"] == "return"]
    assert returns, "Expected at least one return in the month"

    for t in returns:
        assert t["total_amount"] < 0, t["transaction_id"]
        for item in t["items"]:
            assert item["quantity"] < 0, t["transaction_id"]
            assert item["line_total"] < 0, t["transaction_id"]

def test_same_seed_gives_same_output():
    first = generate_month(get_products(), YEAR, MONTH)
    second = generate_month(get_products(), YEAR, MONTH)
    assert first == second