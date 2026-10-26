import pandas as pd

PRODUCTS = [
    {"product_id": "PRD-10001", "product_name": "Brandstation", "category": "Byggklossar", "brand": "LEGO", "age_group": "5-12", "price_sek": 649.00},
    {"product_id": "PRD-10002", "product_name": "Polisstation", "category": "Byggklossar", "brand": "LEGO", "age_group": "5-12", "price_sek": 549.00},
    {"product_id": "PRD-10003", "product_name": "Duplo Tåg", "category": "Byggklossar", "brand": "LEGO", "age_group": "2-5", "price_sek": 399.00},
    {"product_id": "PRD-10004", "product_name": "Gosenalle 30 cm", "category": "Gosedjur", "brand": "Teddykompaniet", "age_group": "0-3", "price_sek": 199.00},
    {"product_id": "PRD-10005", "product_name": "Kanin Mjukis", "category": "Gosedjur", "brand": "Teddykompaniet", "age_group": "0-3", "price_sek": 149.00},
    {"product_id": "PRD-10006", "product_name": "Monopol Sverige", "category": "Sällskapsspel", "brand": "Hasbro", "age_group": "8+", "price_sek": 349.00},
    {"product_id": "PRD-10007", "product_name": "Alfapet", "category": "Sällskapsspel", "brand": "Alga", "age_group": "8+", "price_sek": 299.00},
    {"product_id": "PRD-10008", "product_name": "Uno", "category": "Sällskapsspel", "brand": "Mattel", "age_group": "6+", "price_sek": 99.00},
    {"product_id": "PRD-10009", "product_name": "Radiostyrd bil Turbo", "category": "Fordon", "brand": "Carson", "age_group": "6+", "price_sek": 499.00},
    {"product_id": "PRD-10010", "product_name": "Hot Wheels 5-pack", "category": "Fordon", "brand": "Mattel", "age_group": "3+", "price_sek": 129.00},
    {"product_id": "PRD-10011", "product_name": "Pärlplattor 3000 st", "category": "Pyssel", "brand": "Hama", "age_group": "5+", "price_sek": 129.00},
    {"product_id": "PRD-10012", "product_name": "Modellera 10 färger", "category": "Pyssel", "brand": "Play-Doh", "age_group": "3+", "price_sek": 179.00},
    {"product_id": "PRD-10013", "product_name": "Barbie Dreamhouse", "category": "Dockor", "brand": "Mattel", "age_group": "3+", "price_sek": 1999.00},
    {"product_id": "PRD-10014", "product_name": "Barbie Docka", "category": "Dockor", "brand": "Mattel", "age_group": "3+", "price_sek": 249.00},
    {"product_id": "PRD-10015", "product_name": "Pussel 1000 bitar", "category": "Pussel", "brand": "Ravensburger", "age_group": "12+", "price_sek": 189.00},
]


def get_products() -> pd.DataFrame:
    """Return the store's product catalog as a DataFrame."""
    return pd.DataFrame(PRODUCTS)