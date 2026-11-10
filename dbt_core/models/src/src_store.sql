with src_store as (select * from {{ source('inventory_data', 'inventory') }})

select
    store__store_id as store_id,
    store__store_name as store_name,
    store__store_city as store_city,
    store__store_address as store_address,
    snapshot_timestamp
from src_store