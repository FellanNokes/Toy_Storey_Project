with sales as (select * from {{ ref('fct_sales') }}),
date as (select * from {{ ref('dim_date') }}),

transactions as (
    select
        transaction_id,
        date_id,
        transaction_timestamp,
        transaction_type,
        payment_method,
        customer_id,
        sum(line_total) as total_amount
    from sales
    group by
        transaction_id,
        date_id,
        transaction_timestamp,
        transaction_type,
        payment_method,
        customer_id
)

select
    t.transaction_id,
    d.day,
    d.month,
    d.year,
    d.day_of_week,
    d.date,
    t.total_amount,
    t.payment_method,
    t.transaction_type,
    t.transaction_timestamp,
    t.customer_id
from transactions t
left join date d on t.date_id = d.date_id