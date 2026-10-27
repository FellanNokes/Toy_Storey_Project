import random
from collections import defaultdict
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pandas as pd

from products import get_store

TIMEZONE = ZoneInfo("Europe/Stockholm")
LEAD_TIME_DAYS = 3
DELIVERY_TIME = time(5, 30)
SNAPSHOT_TIME = time(6, 0)
RESERVATION_SHARE = 0.2  # share of products with a customer reservation on a given day


def to_timestamp(day: date, at: time) -> str:
    """Return an ISO timestamp in Stockholm time, e.g. 2025-03-14T06:00:00+01:00."""
    return datetime.combine(day, at, tzinfo=TIMEZONE).isoformat()


def stock_status(on_hand: int, reorder_point: int) -> str:
    """Classify the stock level of one product."""
    if on_hand <= 0:
        return "out_of_stock"
    if on_hand <= reorder_point:
        return "low_stock"
    return "in_stock"


def summarize_sales(transactions: list[dict]) -> dict:
    """Group transactions per date and product.

    Returns {date: {product_id: {"net_quantity": int, "last_sold_at": str | None}}}.
    net_quantity is sold minus returned, since returns have negative quantity.
    """
    summary = defaultdict(lambda: defaultdict(lambda: {"net_quantity": 0, "last_sold_at": None}))
    for transaction in transactions:
        timestamp = datetime.fromisoformat(transaction["transaction_timestamp"])
        day = timestamp.date()
        for item in transaction["items"]:
            entry = summary[day][item["product_id"]]
            entry["net_quantity"] += item["quantity"]
            if transaction["transaction_type"] == "sale":
                if entry["last_sold_at"] is None or timestamp > datetime.fromisoformat(entry["last_sold_at"]):
                    entry["last_sold_at"] = timestamp.isoformat()
    return summary


def build_snapshot(day: date, state: dict, products: list[dict], rng: random.Random) -> dict:
    """Build the inventory snapshot for one morning."""
    store = get_store()
    items = []
    for product in products:
        product_state = state[product["product_id"]]
        on_hand = product_state["on_hand"]

        reserved = 0
        if on_hand > 0 and rng.random() < RESERVATION_SHARE:
            reserved = min(rng.randint(1, 2), on_hand)

        items.append({
            "product_id": product["product_id"],
            "quantity_on_hand": on_hand,
            "quantity_reserved": reserved,
            "quantity_available": on_hand - reserved,
            "quantity_on_order": sum(qty for _, qty in product_state["on_order"]),
            "reorder_point": product["reorder_point"],
            "reorder_quantity": product["reorder_quantity"],
            "stock_status": stock_status(on_hand, product["reorder_point"]),
            "location": product["location"],
            "unit_cost": float(product["unit_cost"]),
            "unit_price": float(product["price_sek"]),
            "last_restocked_at": product_state["last_restocked_at"],
            "last_sold_at": product_state["last_sold_at"],
        })

    return {
        "snapshot_id": f"SNAP-{day:%Y-%m-%d}-{store['store_id']}",
        "snapshot_timestamp": to_timestamp(day, SNAPSHOT_TIME),
        "store": store,
        "items": items,
    }


def simulate_inventory(products: pd.DataFrame, transactions: list[dict], year: int) -> list[dict]:
    """Create one inventory snapshot per day, based on sales up to the day before."""
    rng = random.Random(year)
    product_list = products.to_dict("records")
    sales_per_day = summarize_sales(transactions)

    state = {
        p["product_id"]: {
            "on_hand": int(p["start_stock"]),
            "on_order": [],  # list of (arrival_date, quantity)
            "last_restocked_at": None,
            "last_sold_at": None,
        }
        for p in product_list
    }

    snapshots = []
    day = date(year, 1, 1)
    while day.year == year:
        # 1. Deliver orders that arrive this morning
        for product_state in state.values():
            arriving = [qty for arrival, qty in product_state["on_order"] if arrival == day]
            if arriving:
                product_state["on_hand"] += sum(arriving)
                product_state["on_order"] = [o for o in product_state["on_order"] if o[0] != day]
                product_state["last_restocked_at"] = to_timestamp(day, DELIVERY_TIME)

        # 2. Morning snapshot, before today's sales
        snapshots.append(build_snapshot(day, state, product_list, rng))

        # 3. Apply today's sales and returns
        for product_id, sales in sales_per_day.get(day, {}).items():
            product_state = state[product_id]
            product_state["on_hand"] -= sales["net_quantity"]
            if sales["last_sold_at"]:
                product_state["last_sold_at"] = sales["last_sold_at"]

        # 4. Place orders for products that are running low
        for product in product_list:
            product_state = state[product["product_id"]]
            on_order = sum(qty for _, qty in product_state["on_order"])
            if product_state["on_hand"] + on_order <= product["reorder_point"]:
                arrival = day + timedelta(days=LEAD_TIME_DAYS)
                product_state["on_order"].append((arrival, int(product["reorder_quantity"])))

        day += timedelta(days=1)

    return snapshots