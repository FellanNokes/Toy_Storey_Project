with holidays as(select * from {{ ref('swedish_holidays_2022_2026')}})

select
    date,
    holiday_name,
    holiday_name_en,
    day_of_week,
    is_public_holiday
from holidays