-- Example company: 1 machine, 1 MW, must run 4 hours per day.
-- Normal plan: 08:00–11:59. Flexible plan: the 4 cheapest hours of the day.

with ranked as (
    select
        date_day,
        hour_of_day,
        price_eur_mwh,
        row_number() over (
            partition by date_day
            order by price_eur_mwh
        )                                                       as price_rank   -- 1 = cheapest hour of the day
    from {{ ref('fct_market_hour') }}
    where price_eur_mwh is not null
),

daily as (
    select
        date_day,
        count(*)                                                as price_hours,
        sum(case when hour_of_day between 8 and 11 then price_eur_mwh end) as normal_cost_eur,
        sum(case when price_rank <= 4 then price_eur_mwh end)  as flexible_cost_eur
    from ranked
    group by date_day
)

select
    date_day,
    round(normal_cost_eur, 2)                                   as normal_cost_eur,
    round(flexible_cost_eur, 2)                                 as flexible_cost_eur,
    round(normal_cost_eur - flexible_cost_eur, 2)               as saved_eur
from daily
where price_hours >= 23     -- only full days (23 = the day the clocks change in spring)
