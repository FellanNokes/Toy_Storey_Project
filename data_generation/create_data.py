from export import export_year
from products import get_products
from storage import save_csv

if __name__ == "__main__":
    products = get_products()

    save_csv(products, "products.csv")
    export_year(products, 2025)