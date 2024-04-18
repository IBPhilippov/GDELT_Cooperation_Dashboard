from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



@data_loader
def load_data_from_big_query(*args, **kwargs):
    year = kwargs.get('year')
    print(year)
    query = f"""SELECT DISTINCT GLOBALEVENTID, _PARTITIONTIME as EventTimestamp, MonthYear, Year, EventCode, Actor1CountryCode, Actor2CountryCode, \
     Actor1Type1Code, Actor2Type1Code \
      FROM `gdelt-bq.gdeltv2.events_partitioned`\
      WHERE EXTRACT(YEAR FROM (TIMESTAMP_TRUNC(_PARTITIONTIME, DAY))) = \
      {year} and EventRootCode='06' \
      and IsRootEvent=1 and IFNULL(Actor1CountryCode,'')!=IFNULL(Actor2CountryCode,'')"""
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    return BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
