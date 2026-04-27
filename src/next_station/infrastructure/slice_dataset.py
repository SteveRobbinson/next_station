import rasterio
from rasterio.io import MemoryFile
from typing import List
from rasterio.windows import Window
import requests
import io


def slice_dataset(request = requests.Response,
                  num_chunks: int = 4
                  ) -> List[io.BytesIO]:

    with rasterio.open(io.BytesIO(request.content)) as df:
        
        df_width = df.width
        df_height = df.height
        chunk_height = int(df_height / num_chunks) + 1

        original_profile = df.profile.copy()

        sliced_dataset = []

        for i in range(num_chunks):
            
            win = Window(0, i * chunk_height, df_width, chunk_height)
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


            buf = io.BytesIO()
            
            with MemoryFile() as memfile:
                
                with memfile.open(**current_profile) as tiff:
                    tiff.write(sliced_data, 1)

                final_buffer = io.BytesIO(memfile.read())
                sliced_dataset.append(final_buffer)

        return sliced_dataset

