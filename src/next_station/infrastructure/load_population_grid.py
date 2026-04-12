from pyspark.sql import SparkSession

def load_population_grid(spark: SparkSession,
                         aws_s3_path: str,
                         data_format: str = 'binaryFile'):

    return spark.read.format(data_format).option("pathGlobFilter", "*.tif").load(aws_s3_path)
