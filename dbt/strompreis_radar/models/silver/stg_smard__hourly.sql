{{ config(
    materialized = 'incremental',
    incremental_strategy = 'merge',
    unique_key = ['series_id', 'ts_utc']
) }}

with hours as (
    select
        cast(regexp_extract(_source_file, '/(\\d+)_\\d+\\.json$', 1) as int) as series_id,
        explode(from_json(series, 'array<array<double>>'))                as hour_pair,
        _source_file,
        _load_ts
    from {{ source('bronze', 'smard_raw') }}
    {% if is_incremental() %}
    where _load_ts > (select max(_load_ts) from {{ this }})
    {% endif %}
),

ranked as (
    select
        series_id,
        timestamp_millis(cast(hour_pair[0] as bigint)) as ts_utc,
        hour_pair[1]                                   as value,
        _source_file,
        _load_ts,
        row_number() over (
            partition by series_id, hour_pair[0]
            order by _load_ts desc
        )                                              as version_rank
    from hours
    where hour_pair[1] is not null
)

select
    series_id,
    case series_id
        when 4169 then 'price_day_ahead'
        when 4068 then 'solar'
        when 4067 then 'wind_onshore'
        when 1225 then 'wind_offshore'
        when 410  then 'consumption'
    end                                                 as series_name,
    ts_utc,
    from_utc_timestamp(ts_utc, 'Europe/Berlin')         as ts_berlin,
    value,
    _source_file,
    _load_ts
from ranked
where version_rank = 1

