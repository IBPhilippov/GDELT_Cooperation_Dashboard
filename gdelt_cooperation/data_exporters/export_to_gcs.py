

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
import pyarrow as pa
import pyarrow.parquet as pq
import os
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, **kwargs) -> None:

    year = kwargs.get('year')
    GCS_BUCKET_NAME=kwargs.get('GCS_BUCKET_NAME')
    if GCS_BUCKET_NAME is None:
        GCS_BUCKET_NAME=kwargs['context']['GCS_BUCKET_NAME'] 

    GCP_PROJECT_NAME=kwargs.get('GCP_PROJECT_NAME')
    if GCP_PROJECT_NAME is None:
        GCP_PROJECT_NAME=kwargs['context']['GCP_PROJECT_NAME'] 

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/gdelt_cooperation/credentials.json'
    bucket_name = GCS_BUCKET_NAME
    table_name = 'gdelt'
    object_key = 'gdelt.parquet'
    root_path = f'{bucket_name}/{table_name}_{year}'

    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()

    pq.write_table(table, root_path+'/gdelt.parquet', filesystem=gcs)
    return root_path

    

