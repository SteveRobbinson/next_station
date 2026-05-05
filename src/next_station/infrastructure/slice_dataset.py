import logging
import rasterio
from rasterio.io import MemoryFile
from rasterio.windows import Window
import requests
import io
from next_station.core.exceptions.base import InfrastructureError

logger = logging.getLogger(__name__)

def slice_dataset(request = requests.Response,
                  num_chunks: int = 4
                  ) -> list[io.BytesIO]:

    logger.info(f"Starting slicing population grid dataset to {num_chunks} chunks")

    try:
        with rasterio.open(io.BytesIO(request.content)) as df:
            
            df_width = df.width
            df_height = df.height
            chunk_height = int(df_height / num_chunks) + 1

            original_profile = df.profile.copy()

            sliced_dataset = []

            for i in range(num_chunks):
                logger.info(f"Slicing chunk nr.: {i+1}/{num_chunks}...")

                win = Window(col_off=0,
                             row_off=i * chunk_height,
                             width=df_width,
                             height=chunk_height)

                sliced_data = df.read(1, window=win)

                win_transform = df.window_transform(win)

                current_profile = original_profile.copy()
                current_profile.update({
                    'height': sliced_data.shape[0],
                    'width': sliced_data.shape[1],
                    'transform': win_transform,
                    'tiled': True,
                    'blockxsize': 256,
                    'blockysize': 256
                    })


                with MemoryFile() as memfile:
                    with memfile.open(**current_profile) as tiff:

                        tiff.write(sliced_data, 1)

                    final_buffer = io.BytesIO(memfile.read())
                    sliced_dataset.append(final_buffer)

        logger.info("Successfully sliced population grid dataset")
        return sliced_dataset


    except Exception as err:
        logger.exception("Failed to slice population grid dataset")
        raise InfrastructureError(
                source='### Dataset Slicer ###',
                status_code=500,
                details=f"Slicing failed: {str(err)}"
                )
