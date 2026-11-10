with src_inventory as(select * from {{ ref('src_inventory') }})

select
    store_id,
    store_name,
    store_city,
    store_address
from src_inventory 
-- use the latest row for each product id
qualify row_number() over (
    partition by product_id
    order by updated_at desc
) = 1