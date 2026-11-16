with inventory as (select * from {{ ref('src_inventory') }}),
items as (select * from {{ ref('src_inventory_item') }})

select
    h.snapshot_id,
    upper(trim(i.product_id)) as product_id,
    h.snapshot_timestamp,
    {{ dbt_utils.generate_surrogate_key(['cast(h.snapshot_timestamp as date)']) }} as date_id,
    h.store_id,
    i.shelf_location,
    i.stock_status,
    i.last_sold_at,
    i.last_restocked_at,
    i.quantity_on_hand,
    i.quantity_reserved,
    i.quantity_available,
    i.quantity_on_order,
    i.reorder_point,
    i.unit_cost,
    i.unit_price,
    i.quantity_on_hand * i.unit_cost as inventory_value
from items i
left join inventory h on i._dlt_parent_id = h._dlt_id




