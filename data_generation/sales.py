import calendar
from collections import OrderedDict
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import pandas as pd
from faker import Faker

TIMEZONE = ZoneInfo("Europe/Stockholm")
OPENING_TIME = time(10, 0)
CLOSING_TIME = time(19, 0)

STORE_ID = "STO-001"
CURRENCY = "SEK"
VAT_RATE = 0.25
REGISTERS = ["KASSA-01", "KASSA-02", "KASSA-03"]
EMPLOYEES = ["EMP-0101", "EMP-0102", "EMP-0215", "EMP-0233", "EMP-0457", "EMP-0512"]

PAYMENT_METHODS = OrderedDict([("card", 0.70), ("swish", 0.25), ("cash", 0.05)])
TRANSACTION_TYPES = OrderedDict([("sale", 0.98), ("return", 0.02)])

# Campaign code -> (discount share, months when it is active)
CAMPAIGNS = {
    "VINTER10": (0.10, {1, 2}),
    "SOMMAR15": (0.15, {6, 7, 8}),
    "HOST10": (0.10, {9, 10, 11}),
    "JUL20": (0.20, {12}),
}
CAMPAIGN_SHARE = 0.15
MEMBER_SHARE = 0.40


def create_faker(seed: int | None = None) -> Faker:
    """Create a Faker instance. Use a seed to get the same data every run."""
    fake = Faker("sv_SE")
    if seed is not None:
        Faker.seed(seed)
    return fake


def pick_campaign(fake: Faker, month: int) -> str | None:
    """Return an active campaign code for some transactions, otherwise None."""
    active = [code for code, (_, months) in CAMPAIGNS.items() if month in months]
    if not active or fake.random.random() > CAMPAIGN_SHARE:
        return None
    return fake.random_element(active)


def build_items(fake: Faker, products: list[dict], discount_share: float, sign: int) -> list[dict]:
    """Create 1-4 receipt lines. sign is -1 for returns."""
    n_items = fake.random_int(min=1, max=4)
    chosen = fake.random_elements(elements=products, length=n_items, unique=True)

    items = []
    for line_number, product in enumerate(chosen, start=1):
        quantity = fake.random_int(min=1, max=3) * sign
        unit_price = float(product["price_sek"])
        discount_amount = round(unit_price * quantity * discount_share, 2) + 0.0  # avoid -0.0
        items.append({
            "line_number": line_number,
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_amount": discount_amount,
            "vat_rate": VAT_RATE,
            "line_total": round(unit_price * quantity - discount_amount, 2),
        })
    return items


def generate_transaction(fake: Faker, products: list[dict], timestamp: datetime, number: int) -> dict:
    """Create one transaction (a receipt) at the given time."""
    transaction_type = fake.random_element(TRANSACTION_TYPES)
    sign = -1 if transaction_type == "return" else 1
    campaign_code = pick_campaign(fake, timestamp.month) if sign == 1 else None
    discount_share = CAMPAIGNS[campaign_code][0] if campaign_code else 0.0
    is_member = fake.random.random() < MEMBER_SHARE

    items = build_items(fake, products, discount_share, sign)
    subtotal = round(sum(i["unit_price"] * i["quantity"] for i in items), 2)
    total_discount = round(sum(i["discount_amount"] for i in items), 2)
    total_amount = round(subtotal - total_discount, 2)

    return {
        "transaction_id": f"TXN-{timestamp:%Y-%m-%d}-{number:06d}",
        "transaction_timestamp": timestamp.isoformat(),
        "transaction_type": transaction_type,
        "store_id": STORE_ID,
        "register_id": fake.random_element(REGISTERS),
        "employee_id": fake.random_element(EMPLOYEES),
        "customer_id": f"CUST-{fake.random_int(10000, 99999)}" if is_member else None,
        "items": items,
        "campaign_code": campaign_code,
        "payment_method": fake.random_element(PAYMENT_METHODS),
        "currency": CURRENCY,
        "subtotal": subtotal,
        "total_discount": total_discount,
        "vat_amount": round(total_amount * VAT_RATE / (1 + VAT_RATE), 2),
        "total_amount": total_amount,
    }


def generate_day(fake: Faker, products: list[dict], day: date) -> list[dict]:
    """Create all transactions for one day. More customers on weekends."""
    is_weekend = day.weekday() >= 5
    n_transactions = fake.random_int(min=40, max=80) if is_weekend else fake.random_int(min=20, max=50)

    opening = datetime.combine(day, OPENING_TIME)
    closing = datetime.combine(day, CLOSING_TIME)
    times = sorted(
        fake.date_time_between_dates(opening, closing).replace(microsecond=0, tzinfo=TIMEZONE)
        for _ in range(n_transactions)
    )
    return [generate_transaction(fake, products, ts, number) for number, ts in enumerate(times, start=1)]


def generate_month(products: pd.DataFrame, year: int, month: int) -> list[dict]:
    """Create all transactions for one month. The seed is based on the month."""
    fake = create_faker(seed=year * 100 + month)
    product_list = products.to_dict("records")
    last_day = calendar.monthrange(year, month)[1]

    transactions = []
    for day_number in range(1, last_day + 1):
        transactions.extend(generate_day(fake, product_list, date(year, month, day_number)))
    return transactions