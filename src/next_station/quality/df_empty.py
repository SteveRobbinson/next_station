from pyspark.sql import DataFrame

def is_df_empty(df: DataFrame) -> DataFrame:

    if df.isEmpty():
        raise ValueError('Dataframe is empty')
    
    return df
