from databricks.connect import DatabricksSession
from pyspark.sql import SparkSession

def get_spark_session(profile_name: str = 'DEFAULT') -> SparkSession:

    spark = DatabricksSession.builder.serverless().profile(profile_name).getOrCreate()

    return spark

