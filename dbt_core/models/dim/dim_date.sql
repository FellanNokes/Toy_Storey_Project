with date_spine as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2025-01-01' as date)",
        end_date="cast('2027-01-01' as date)"
    ) }}
), 
holidays as(select * from {{ ref('swedish_holidays_2022_2026')}})

select
    cast(date_day as date) as date,
    {{ dbt_utils.generate_surrogate_key(['date']) }} as date_id,
    year(date_day) as year,
    month(date_day) as month,
    day(date_day) as day,
    dayname(date_day) as day_of_week,
    isodow(date_day) in (6, 7) as is_weekend,
    h.date is not null as is_holiday
from date_spine d
left join holidays h on d.date = cast(h.date as date)