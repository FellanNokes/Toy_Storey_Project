with src_products as(select * from {{ ref('src_products') }})

select
    product_id,
    product_name,
    category,
    brand,
    age_group,
    start_stock,
    reorder_point,
    reorder_quantity
from src_products 
-- use the latest row for each product id
qualify row_number() over (
    partition by product_id
    order by updated_at desc
) = 1