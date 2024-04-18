from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pyarrow as pa
import pyarrow.parquet as pq
import os
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(data,*args, **kwargs):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/gdelt_cooperation/credentials.json'

    gcs = pa.fs.GcsFileSystem()
    arrow_df = pa.parquet.ParquetDataset(f'{data}', filesystem=gcs)

    return arrow_df.read().to_pandas()



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
