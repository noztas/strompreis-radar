-- Fails if any series has the same hour more than once.
select
    series_id,
    ts_utc,
    count(*) as n_rows
from {{ ref('stg_smard__hourly') }}
group by series_id, ts_utc
having count(*) > 1
