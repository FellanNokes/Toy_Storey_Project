with sales AS (select * from {{ ref('fct_sales') }}),
date AS (select * from {{ ref('dim_date') }})

select
    d.day,
    d.month,
    d.year,
    d.day_of_week,
    d.date,
    s.total_amount,
    s.payment_method,
    s.transaction_type,
    s.transaction_timestamp,
    s.customer_id
from sales s
left join date d on s.date_id = d.date_id