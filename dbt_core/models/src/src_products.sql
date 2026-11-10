with stg_products as(select * from {{ source('products_data', 'products') }})

select
    product_id,
    product_name,
    category,
    brand,
    age_group,
    start_stock,
    reorder_point,
    reorder_quantity,
    location as shelf_location
from stg_products