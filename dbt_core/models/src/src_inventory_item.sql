with stg_inventory_items as (select * from {{ source('inventory_items_data', 'inventory__items') }})

select
    product_id,
    location as shelf_location,
    quantity_on_hand,
    quantity_reserved,
    quantity_available,
    quantity_on_order,
    reorder_point,
    stock_status,
    last_sold_at,
    last_restocked_at,
    unit_cost,
    unit_price,
    _dlt_parent_id
from stg_inventory_items