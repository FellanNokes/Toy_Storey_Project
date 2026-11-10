with header as (
    select * from {{ source('inventory_data', 'inventory') }}
),
items as (
    select * from {{ source('inventory_items_data', 'inventory__items') }}
)

select
    h.snapshot_id,
    h.snapshot_timestamp,
    cast(h.snapshot_timestamp as date) as snapshot_date,
    h.store__store_id as store_id,
    upper(trim(i.product_id)) as product_id,
    i.location as shelf_location,
    i.quantity_on_hand,
    i.quantity_reserved,
    i.quantity_available,
    i.quantity_on_order,
    i.stock_status,
    i.last_sold_at,
    i.last_restocked_at,
    i.unit_cost,
    i.unit_price
from items i
join header h on i._dlt_parent_id = h._dlt_id