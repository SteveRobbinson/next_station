from next_station.core.spark import get_spark_session
from next_station.infrastructure.load_population_grid import load_population_grid
from next_station.core.config.settings import settings
from next_station.infrastructure.databricks import save_df_in_db
from sedona.spark import SedonaContext
from next_station.quality.extract_population_grid import extract_population_points

spark_session = get_spark_session(settings.databricks.compute_config)

spark_session = SedonaContext.create(spark_session)

raw_df = load_population_grid(spark_session,
                              settings.aws.population_grid_uri)

df_exploded = extract_population_points(raw_df)

save_df_in_db(df_exploded, settings.databricks.population_grid_bronze_fqn)
