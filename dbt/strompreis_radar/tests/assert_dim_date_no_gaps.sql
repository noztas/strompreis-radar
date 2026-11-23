-- No missing days in dim_date.
-- If every day from the first to the last day is there, then
-- number of rows = (last day - first day) + 1.
-- Together with the unique test on date_day, this proves: no gaps.
-- Returns 1 row (= FAIL) if the numbers don't match, 0 rows (= PASS) if they do.

select
    count(*)                                        as actual_days,
    datediff(max(date_day), min(date_day)) + 1      as expected_days
from {{ ref('dim_date') }}
having count(*) <> datediff(max(date_day), min(date_day)) + 1
