with bounds as (
    select
        min(to_date(ts_berlin))              as first_day,
        date_add(max(to_date(ts_berlin)), 7) as last_day     -- +7 days for the forecast later
    from {{ ref('stg_smard__hourly') }}
),

days as (
    select explode(sequence(first_day, last_day, interval 1 day)) as date_day
    from bounds
)

select
    d.date_day,
    year(d.date_day)                                   as year,
    quarter(d.date_day)                                as quarter,
    month(d.date_day)                                  as month,
    date_format(d.date_day, 'MMMM')                    as month_name,
    dayofmonth(d.date_day)                             as day_of_month,
    weekday(d.date_day) + 1                            as weekday_number,   -- 1 = Monday … 7 = Sunday
    date_format(d.date_day, 'EEEE')                    as weekday_name,
    weekday(d.date_day) >= 5                           as is_weekend,
    h.holiday_date is not null                         as is_holiday,
    h.holiday_name,
    weekday(d.date_day) < 5 and h.holiday_date is null as is_working_day
from days d
left join {{ ref('german_holidays') }} h
    on d.date_day = cast(h.holiday_date as date)
