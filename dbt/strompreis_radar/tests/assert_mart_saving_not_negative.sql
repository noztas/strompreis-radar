select date_day, saved_eur
from {{ ref('mart_load_shift') }}
where saved_eur < 0