from databricks.connect import DatabricksSession
from pyspark.sql import SparkSession

def get_spark_session() -> SparkSession:

    spark = DatabricksSession.builder.getOrCreate()

    return spark
