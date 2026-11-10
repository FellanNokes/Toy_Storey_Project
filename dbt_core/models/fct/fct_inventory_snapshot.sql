with inventory as (
    select * from {{ ref('src_inventory') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['snapshot_date']) }} as date_id,
    store_id,
    product_id,
    snapshot_timestamp,
    shelf_location,
    stock_status,
    last_sold_at,
    last_restocked_at,
    quantity_on_hand,
    quantity_reserved,
    quantity_available,
    quantity_on_order,
    unit_cost,
    unit_price,
    quantity_on_hand * unit_cost as inventory_value
from inventory




