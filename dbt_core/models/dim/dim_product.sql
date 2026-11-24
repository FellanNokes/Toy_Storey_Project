with src_products as(select * from {{ ref('src_products') }})

select
    upper(trim(product_id)) as product_id,
    product_name,
    category,
    brand,
    age_group,
    try_cast(split_part(replace(age_group, '+', ''), '-', 1) as integer) as age_min,
    case
        when age_group like '%-%' then try_cast(split_part(age_group, '-', 2) as integer)
        else 99
    end as age_max,
    start_stock,
    reorder_point,
    reorder_quantity
from src_products 
-- use the latest row for each product id
qualify row_number() over (
    partition by product_id
    order by _dlt_load_id desc
) = 1