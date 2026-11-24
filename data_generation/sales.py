import calendar
from collections import OrderedDict
from datetime import date, datetime, time, timedelta
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

# Base number of transactions per day (min, max)
WEEKDAY_TRANSACTIONS = (20, 50)
WEEKEND_TRANSACTIONS = (40, 80)

PAYDAY = 25            # Swedish payday
PAYDAY_DAYS = 4        # payday and the days after it sell more
PAYDAY_FACTOR = 1.25

BLACK_FRIDAY_FACTOR = 2.5
BLACK_WEEK_FACTOR = 1.4

# Seasonal factor per category: {category: {month: factor}}. Missing months = 1.0
SEASONAL_FACTORS = {
    "Pussel": {1: 1.5, 2: 1.4, 11: 1.3, 12: 1.3, 6: 0.7, 7: 0.6, 8: 0.7},
    "Sällskapsspel": {1: 1.3, 2: 1.2, 11: 1.3, 12: 1.5, 6: 0.8, 7: 0.7, 8: 0.8},
    "Pyssel": {1: 1.2, 2: 1.4, 3: 1.2, 6: 0.8, 7: 0.7},
    "Fordon": {5: 1.3, 6: 1.5, 7: 1.5, 8: 1.3, 1: 0.8, 2: 0.8},
    "Byggklossar": {12: 1.3},
}


def create_faker(seed: int | None = None) -> Faker:
    """Create a Faker instance. Use a seed to get the same data every run."""
    fake = Faker("sv_SE")
    if seed is not None:
        Faker.seed(seed)
    return fake


def black_friday(year: int) -> date:
    """Black Friday is the day after the fourth Thursday in November."""
    first = date(year, 11, 1)
    first_thursday = first + timedelta(days=(3 - first.weekday()) % 7)
    return first_thursday + timedelta(weeks=3, days=1)


def day_factor(day: date) -> float:
    """How much busier this day is than a normal day."""
    factor = 1.0

    bf = black_friday(day.year)
    if day == bf:
        factor *= BLACK_FRIDAY_FACTOR
    elif bf - timedelta(days=4) <= day <= bf + timedelta(days=3):
        factor *= BLACK_WEEK_FACTOR

    if day.month == 12 and day.day <= 23:
        factor *= 1.3 + 1.2 * (day.day - 1) / 22   # ramps from 1.3 to 2.5 before Christmas

    if PAYDAY <= day.day < PAYDAY + PAYDAY_DAYS:
        factor *= PAYDAY_FACTOR

    return factor


def product_weights(products: list[dict], month: int) -> list[float]:
    """Popularity weight per product, adjusted for the season of its category."""
    return [
        p["popularity_weight"] * SEASONAL_FACTORS.get(p["category"], {}).get(month, 1.0)
        for p in products
    ]


def pick_products(fake: Faker, products: list[dict], weights: list[float], n: int) -> list[dict]:
    """Pick n different products, where a higher weight means a higher chance."""
    pool = list(zip(products, weights))
    chosen = []
    for _ in range(min(n, len(pool))):
        index = fake.random.choices(range(len(pool)), weights=[w for _, w in pool])[0]
        chosen.append(pool.pop(index)[0])
    return chosen


def pick_campaign(fake: Faker, month: int) -> str | None:
    """Return an active campaign code for some transactions, otherwise None."""
    active = [code for code, (_, months) in CAMPAIGNS.items() if month in months]
    if not active or fake.random.random() > CAMPAIGN_SHARE:
        return None
    return fake.random_element(active)


def build_items(fake: Faker, products: list[dict], weights: list[float], discount_share: float, sign: int) -> list[dict]:
    """Create 1-4 receipt lines. sign is -1 for returns."""
    n_items = fake.random_int(min=1, max=4)
    chosen = pick_products(fake, products, weights, n_items)

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


def generate_transaction(fake: Faker, products: list[dict], weights: list[float], timestamp: datetime, number: int) -> dict:
    """Create one transaction (a receipt) at the given time."""
    transaction_type = fake.random_element(TRANSACTION_TYPES)
    sign = -1 if transaction_type == "return" else 1
    campaign_code = pick_campaign(fake, timestamp.month) if sign == 1 else None
    discount_share = CAMPAIGNS[campaign_code][0] if campaign_code else 0.0
    is_member = fake.random.random() < MEMBER_SHARE

    items = build_items(fake, products, weights, discount_share, sign)
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
    """Create all transactions for one day. Busier on weekends, holidays and after payday."""
    low, high = WEEKEND_TRANSACTIONS if day.weekday() >= 5 else WEEKDAY_TRANSACTIONS
    n_transactions = round(fake.random_int(min=low, max=high) * day_factor(day))
    weights = product_weights(products, day.month)

    opening = datetime.combine(day, OPENING_TIME)
    closing = datetime.combine(day, CLOSING_TIME)
    times = sorted(
        fake.date_time_between_dates(opening, closing).replace(microsecond=0, tzinfo=TIMEZONE)
        for _ in range(n_transactions)
    )
    return [generate_transaction(fake, products, weights, ts, number) for number, ts in enumerate(times, start=1)]


def generate_month(products: pd.DataFrame, year: int, month: int) -> list[dict]:
    """Create all transactions for one month. The seed is based on the month."""
    fake = create_faker(seed=year * 100 + month)
    product_list = products.to_dict("records")
    last_day = calendar.monthrange(year, month)[1]

    transactions = []
    for day_number in range(1, last_day + 1):
        transactions.extend(generate_day(fake, product_list, date(year, month, day_number)))
    return transactions