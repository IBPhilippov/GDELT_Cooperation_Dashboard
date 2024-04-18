import os
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from mage_ai.data_preparation.variable_manager import set_global_variable

from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data(*args, **kwargs):

    spark = (
        SparkSession
        .builder
        .appName('spark local')
        .getOrCreate()
    )
    kwargs['context']['spark'] = spark
    with open('/home/src/environment.env') as f:
        for line in f.readlines():
            if line.find('GCP_PROJECT_NAME=')>-1:
                GCP_PROJECT_NAME=line.split('GCP_PROJECT_NAME=')[1][:-1]
                kwargs['context']['GCP_PROJECT_NAME'] = GCP_PROJECT_NAME

            if line.find('BQ_DATASET_NAME=')>-1:
                BQ_DATASET_NAME=line.split('BQ_DATASET_NAME=')[1][:-1]
                kwargs['context']['BQ_DATASET_NAME'] = BQ_DATASET_NAME

            if line.find('ADDITIONAL_PART=')>-1:
                ADDITIONAL_PART=line.split('ADDITIONAL_PART=')[1][:-1]
                kwargs['context']['ADDITIONAL_PART'] = ADDITIONAL_PART
    set_global_variable(kwargs.get('pipeline_uuid'), 'GCS_BUCKET_NAME',  str(GCP_PROJECT_NAME)+str(BQ_DATASET_NAME)+str(ADDITIONAL_PART))
    kwargs['context']['GCS_BUCKET_NAME'] = str(GCP_PROJECT_NAME)+str(BQ_DATASET_NAME)+str(ADDITIONAL_PART)

    set_global_variable(kwargs.get('pipeline_uuid'), 'GCS_BUCKET_NAME',  str(GCP_PROJECT_NAME)+str(BQ_DATASET_NAME)+str(ADDITIONAL_PART))
    set_global_variable(kwargs.get('pipeline_uuid'), 'ADDITIONAL_PART',  ADDITIONAL_PART)
    set_global_variable(kwargs.get('pipeline_uuid'), 'BQ_DATASET_NAME',  BQ_DATASET_NAME)
    set_global_variable(kwargs.get('pipeline_uuid'), 'GCP_PROJECT_NAME',  GCP_PROJECT_NAME)


