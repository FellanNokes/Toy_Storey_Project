with stg_sales as (select * from {{ source('sales_data', 'sales') }})

select
    total_amount,
    payment_method,
    transaction_type,
    date(transaction_timestamp) AS date,
    transaction_timestamp,
    customer_id
from stg_sales