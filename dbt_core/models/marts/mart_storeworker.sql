with inventory as (select * from {{ ref('fct_inventory_snapshot') }}),
products as (select * from {{ ref('dim_product') }})

select
    p.product_name,
    p.category,
    p.brand,
    p.age_group,
    i.unit_price,
    i.shelf_location,
    i.quantity_available
from inventory i
left join products p on i.product_id = p.product_id