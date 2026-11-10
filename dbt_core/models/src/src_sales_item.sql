with stg_sales as (select * from {{ source('sales_items_data', 'sales__items') }})

select
    line_number,
    product_id,
    quantity,
    unit_price,
    discount_amount,
    vat_rate,
    line_total,
    _dlt_parent_id,
    _dlt_id
from stg_sales