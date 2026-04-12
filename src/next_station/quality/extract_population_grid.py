from pyspark.sql import DataFrame

def extract_population_points(df: DataFrame,
                              num_partitions: int = 8) -> DataFrame:
    
    df_with_raster = df.selectExpr('RS_FromGeoTiff(content) as raster')
    
    df_tiled = df_with_raster.selectExpr('RS_Tile(raster, 256, 256) as tiles')

    df_distributed = df_tiled.selectExpr('explode(tiles) as tile').repartition(num_partitions)

    df_exploded = df_distributed.selectExpr(
        'explode(RS_PixelAsCentroids(tile, 1)) as exploded'
    ).selectExpr(
            'ST_AsBinary(exploded.geom) as geom_wkb',
            'exploded.value as value'
    )

    return df_exploded

