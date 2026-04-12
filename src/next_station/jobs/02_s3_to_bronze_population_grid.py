from src.next_station.core.spark import get_spark_session
from src.next_station.infrastructure.load_population_grid import load_population_grid
from src.next_station.core.config import settings
from src.next_station.infrastructure.databricks import save_df_in_db
from sedona.spark import SedonaContext
from pyspark.sql import SparkSession
from src.next_station.quality.extract_population_grid import extract_population_points

spark_session = get_spark_session(settings.databricks_python_user_name)

spark_session = SedonaContext.create(spark_session)

raw_df = load_population_grid(spark_session,
                              settings.aws_population_grid_uri)

df_exploded = extract_population_points(raw_df)

save_df_in_db(df_exploded, settings.databricks_population_grid_table_id)
