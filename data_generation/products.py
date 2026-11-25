import pandas as pd

STORE = {
    "store_id": "STO-001",
    "store_name": "Toy Storey",
    "store_city": "Stockholm",
    "store_address": "Götgatan 12, 118 46 Stockholm",
}

# Shelf locations: A = Byggklossar, B = Sällskapsspel, C = Gosedjur,
# D = Fordon, E = Pyssel/Pussel, F = Dockor
# popularity_weight: relative chance of being picked for a receipt (higher = sells more)
PRODUCTS = [
    {"product_id": "PRD-10001", "product_name": "Brandstation", "category": "Byggklossar", "brand": "LEGO", "age_group": "5-12", "price_sek": 649.00,
     "unit_cost": 390.00, "start_stock": 590, "reorder_point": 250, "reorder_quantity": 340, "location": "A-01", "popularity_weight": 10},
    {"product_id": "PRD-10002", "product_name": "Polisstation", "category": "Byggklossar", "brand": "LEGO", "age_group": "5-12", "price_sek": 549.00,
     "unit_cost": 330.00, "start_stock": 580, "reorder_point": 260, "reorder_quantity": 320, "location": "A-02", "popularity_weight": 9},
    {"product_id": "PRD-10003", "product_name": "Duplo Tåg", "category": "Byggklossar", "brand": "LEGO", "age_group": "2-5", "price_sek": 399.00,
     "unit_cost": 240.00, "start_stock": 480, "reorder_point": 230, "reorder_quantity": 250, "location": "A-03", "popularity_weight": 7},
    {"product_id": "PRD-10004", "product_name": "Gosenalle 30 cm", "category": "Gosedjur", "brand": "Teddykompaniet", "age_group": "0-3", "price_sek": 199.00,
     "unit_cost": 90.00, "start_stock": 350, "reorder_point": 140, "reorder_quantity": 210, "location": "C-01", "popularity_weight": 6},
    {"product_id": "PRD-10005", "product_name": "Kanin Mjukis", "category": "Gosedjur", "brand": "Teddykompaniet", "age_group": "0-3", "price_sek": 149.00,
     "unit_cost": 65.00, "start_stock": 310, "reorder_point": 130, "reorder_quantity": 180, "location": "C-02", "popularity_weight": 5},
    {"product_id": "PRD-10006", "product_name": "Monopol Sverige", "category": "Sällskapsspel", "brand": "Hasbro", "age_group": "8+", "price_sek": 349.00,
     "unit_cost": 190.00, "start_stock": 320, "reorder_point": 160, "reorder_quantity": 160, "location": "B-01", "popularity_weight": 4},
    {"product_id": "PRD-10007", "product_name": "Alfapet", "category": "Sällskapsspel", "brand": "Alga", "age_group": "8+", "price_sek": 299.00,
     "unit_cost": 160.00, "start_stock": 230, "reorder_point": 110, "reorder_quantity": 120, "location": "B-02", "popularity_weight": 3},
    {"product_id": "PRD-10008", "product_name": "Uno", "category": "Sällskapsspel", "brand": "Mattel", "age_group": "6+", "price_sek": 99.00,
     "unit_cost": 45.00, "start_stock": 650, "reorder_point": 330, "reorder_quantity": 320, "location": "B-03", "popularity_weight": 9},
    {"product_id": "PRD-10009", "product_name": "Radiostyrd bil Turbo", "category": "Fordon", "brand": "Carson", "age_group": "6+", "price_sek": 499.00,
     "unit_cost": 270.00, "start_stock": 230, "reorder_point": 100, "reorder_quantity": 130, "location": "D-01", "popularity_weight": 3},
    {"product_id": "PRD-10010", "product_name": "Hot Wheels 5-pack", "category": "Fordon", "brand": "Mattel", "age_group": "3+", "price_sek": 129.00,
     "unit_cost": 60.00, "start_stock": 500, "reorder_point": 200, "reorder_quantity": 300, "location": "D-02", "popularity_weight": 8},
    {"product_id": "PRD-10011", "product_name": "Pärlplattor 3000 st", "category": "Pyssel", "brand": "Hama", "age_group": "5+", "price_sek": 129.00,
     "unit_cost": 55.00, "start_stock": 440, "reorder_point": 200, "reorder_quantity": 240, "location": "E-01", "popularity_weight": 7},
    {"product_id": "PRD-10012", "product_name": "Modellera 10 färger", "category": "Pyssel", "brand": "Play-Doh", "age_group": "3+", "price_sek": 179.00,
     "unit_cost": 80.00, "start_stock": 400, "reorder_point": 180, "reorder_quantity": 220, "location": "E-02", "popularity_weight": 6},
    {"product_id": "PRD-10013", "product_name": "Barbie Dreamhouse", "category": "Dockor", "brand": "Mattel", "age_group": "3+", "price_sek": 1999.00,
     "unit_cost": 1200.00, "start_stock": 80, "reorder_point": 40, "reorder_quantity": 40, "location": "F-01", "popularity_weight": 1},
    {"product_id": "PRD-10014", "product_name": "Barbie Docka", "category": "Dockor", "brand": "Mattel", "age_group": "3+", "price_sek": 249.00,
     "unit_cost": 120.00, "start_stock": 430, "reorder_point": 180, "reorder_quantity": 250, "location": "F-02", "popularity_weight": 7},
    {"product_id": "PRD-10015", "product_name": "Pussel 1000 bitar", "category": "Pussel", "brand": "Ravensburger", "age_group": "12+", "price_sek": 189.00,
     "unit_cost": 85.00, "start_stock": 280, "reorder_point": 130, "reorder_quantity": 150, "location": "E-03", "popularity_weight": 4},
]


def get_products() -> pd.DataFrame:
    """Return the store's product catalog as a DataFrame."""
    return pd.DataFrame(PRODUCTS)


def get_store() -> dict:
    """Return the store's details."""
    return STORE