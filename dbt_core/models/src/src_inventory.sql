with stg_inventory as (select * from {{ source('inventory_data', 'inventory') }})

select
    snapshot_id,
    snapshot_timestamp,
    store__store_id as store_id,
    _dlt_id
from stg_inventory