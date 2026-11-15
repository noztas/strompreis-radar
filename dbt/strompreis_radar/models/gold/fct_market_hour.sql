with pivoted as (
    select
        ts_utc,
        ts_berlin,
        max(case when series_name = 'price_day_ahead' then value end) as price_eur_mwh,
        max(case when series_name = 'solar'           then value end) as solar_mwh,
        max(case when series_name = 'wind_onshore'    then value end) as wind_onshore_mwh,
        max(case when series_name = 'wind_offshore'   then value end) as wind_offshore_mwh,
        max(case when series_name = 'consumption'     then value end) as consumption_mwh
    from {{ ref('stg_smard__hourly') }}
    group by ts_utc, ts_berlin
)

select
    ts_utc,
    ts_berlin,
    to_date(ts_berlin)                                  as date_day,      -- key to dim_date
    hour(ts_berlin)                                     as hour_of_day,   -- key to dim_hour
    price_eur_mwh,
    solar_mwh,
    wind_onshore_mwh,
    wind_offshore_mwh,
    consumption_mwh,
    solar_mwh + wind_onshore_mwh + wind_offshore_mwh    as renewable_mwh,
    (solar_mwh + wind_onshore_mwh + wind_offshore_mwh)
        / nullif(consumption_mwh, 0)                    as renewable_share
from pivoted
