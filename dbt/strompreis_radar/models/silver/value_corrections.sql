{{ config(materialized = 'table') }}

with changes as (
    select *
    from table_changes('{{ ref("stg_smard__hourly") }}', 12)
),

pre as (
    select * from changes where _change_type = 'update_preimage'
),

post as (
    select * from changes where _change_type = 'update_postimage'
)

select
    pre.series_id,
    pre.series_name,
    pre.ts_utc,
    pre.ts_berlin,
    pre.value                           as old_value,
    post.value                          as new_value,
    round(post.value - pre.value, 2)    as difference,
    post._commit_version                as commit_version,
    post._commit_timestamp              as corrected_at
from pre
join post
  on  pre.series_id       = post.series_id
  and pre.ts_utc          = post.ts_utc
  and pre._commit_version = post._commit_version
where pre.value <> post.value
