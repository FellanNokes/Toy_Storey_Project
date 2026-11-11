with stg_sales as (select * from {{ source('sales_data', 'sales') }})

select
    transaction_id,
    transaction_timestamp,
    store_id,
    customer_id,
    employee_id,
    campaign_code,
    register_id,
    payment_method,
    transaction_type,
    currency,
    subtotal,
    vat_amount,
    _dlt_id
from stg_sales