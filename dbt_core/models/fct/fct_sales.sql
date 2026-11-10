with sales AS (select * from {{ ref('src_sales') }}),
items AS (select * from {{ ref('src_sales_item') }})

select
    s.transaction_id,
    i.line_number,
    s.transaction_timestamp,
    {{ dbt_utils.generate_surrogate_key(['cast(s.transaction_timestamp as date)']) }} as date_id,
    s.store_id,
    i.product_id,
    s.customer_id,
    s.employee_id,
    s.campaign_code,
    s.register_id,
    s.payment_method,
    s.currency,
    i.quantity,
    i.unit_price,
    i.discount_amount,
    i.vat_rate,
    s.vat_amount,
    i.line_total
from items i
left join sales s on i._dlt_parent_id = s._dlt_id
