with date_spine as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2025-01-01' as date)",
        end_date="cast('2027-01-01' as date)"
    ) }}
), 
src_holiday as(select * from {{ ref('src_holiday')}})

select
    cast(d.date_day as date) as date,
    {{ dbt_utils.generate_surrogate_key(['cast(d.date_day as date)']) }} as date_id,
    year(d.date_day) as year,
    month(d.date_day) as month,
    day(d.date_day) as day,
    dayname(d.date_day) as day_of_week,
    isodow(d.date_day) in (6, 7) as is_weekend,
    h.date is not null as is_holiday
from date_spine d
left join (
    -- remove duplicate dates from src_holiday
    select distinct cast(date as date) as date
    from src_holiday
) h on cast(d.date_day as date) = h.date