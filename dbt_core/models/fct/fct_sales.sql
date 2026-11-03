with sales AS (select * from {{ ref('src_sales') }})

select
    {{ dbt_utils.generate_surrogate_key(['date']) }} AS date_id, 
    date,   
    total_amount,
    payment_method,
    transaction_type,
    transaction_timestamp,
    customer_id
from sales