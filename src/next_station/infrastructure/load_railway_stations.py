from pyspark.sql import SparkSession, DataFrame

def load_json_source(spark: SparkSession,
                     aws_s3_path: str,
                     data_format: str = 'json'
                     ) -> DataFrame:

    return spark.read.format(data_format).option('multiLine', 'true').load(aws_s3_path)
