with src_store as(select * from {{ ref('src_store') }})

select
    store_id,
    store_name,
    store_city,
    store_address
from src_store 
-- use the latest row for each product id
qualify row_number() over (
    partition by store_id
    order by snapshot_timestamp desc
) = 1