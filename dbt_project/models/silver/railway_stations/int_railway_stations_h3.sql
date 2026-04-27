select
  {% for h3_res in var('h3_resolutions') %}
  h3_longlatash3(longitude, latitude, {{h3_res}}) as h3_index_{{h3_res}}
  {%- if not loop.last %},{% endif %} 
  {% endfor %}
from {{ ref('stg_railway_stations') }}
