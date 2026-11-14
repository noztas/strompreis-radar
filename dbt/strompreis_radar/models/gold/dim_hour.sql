select
    h                                       as hour_of_day,
    lpad(cast(h as string), 2, '0') || ':00' as hour_label,
    case
        when h between 0 and 5   then 'night'
        when h between 6 and 11  then 'morning'
        when h between 12 and 17 then 'afternoon'
        else 'evening'
    end                                     as day_part
from (select explode(sequence(0, 23)) as h)
