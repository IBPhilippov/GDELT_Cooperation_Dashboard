from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path
import json

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(df: DataFrame, *args, **kwargs) -> None:
    import os
    import numpy as np
    from google.cloud import bigquery


    GCP_PROJECT_NAME=kwargs.get('GCP_PROJECT_NAME')
    if GCP_PROJECT_NAME is None:
        GCP_PROJECT_NAME=kwargs['context']['GCP_PROJECT_NAME'] 
    BQ_DATASET_NAME=kwargs.get('BQ_DATASET_NAME')
    if BQ_DATASET_NAME is None:
        BQ_DATASET_NAME=kwargs['context']['BQ_DATASET_NAME'] 
    table_id = GCP_PROJECT_NAME+"."+BQ_DATASET_NAME+".events"
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    year = kwargs.get('year')
    df['MonthYear']=df['MonthYear'].astype(str)
    df['Year']=df['Year'].astype(str)

    client = bigquery.Client.from_service_account_json('/home/src/gdelt_cooperation/credentials.json')

    query_job = client.query(
        f'DELETE FROM `{table_id}` WHERE year={year}'
    )



    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        table_id,
        if_exists='append'

    )


    

