with h3_base as (
  select
    population_value,
    {%- for h3_res in var('h3_resolutions') %}
    h3_pointash3(geom_wkb, {{h3_res}}) as h3_index_{{h3_res}}
    {%- if not loop.last %},{% endif %}
    {% endfor %}
  from {{ ref('stg_population_grid') }}
)

select
  *,
  {% for h3_res in var('h3_resolutions') %}
  sum(population_value) over(partition by h3_index_{{h3_res}}) as total_population_{{h3_res}}
  {%- if not loop.last %},{% endif %}
  {% endfor %}
from h3_base
