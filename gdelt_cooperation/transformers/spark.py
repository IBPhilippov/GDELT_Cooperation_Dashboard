if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from pyspark.sql import functions as F
from pyspark.sql import types




@transformer
def transform(data, data_2, data_3, *args, **kwargs):
    try:
        spark = kwargs.get('spark')
        data = spark.createDataFrame(data)
    except:
        spark=kwargs['context']['spark'] 
        data = spark.createDataFrame(data)

    data_2 = spark.createDataFrame(data_2)
    data_3 = spark.createDataFrame(data_3)
    data_4 = spark.read.csv("/home/src/gdelt_cooperation/CAMEO.actionType.txt",sep='\t',header=True)

    data_3=data_3.join(data,data_3.Actor1CountryCode==data.CODE, how='left').withColumnRenamed("LABEL", "Actor1Country").drop('CODE')
    data=data_3.join(data,data_3.Actor2CountryCode==data.CODE,how='left').withColumnRenamed("LABEL", "Actor2Country").drop('CODE')
    data=data.join(data_2,data.Actor1Type1Code==data_2.CODE, how='left').withColumnRenamed("LABEL", "Actor1Type1").drop('CODE')
    data=data.join(data_2,data.Actor2Type1Code==data_2.CODE,how='left').withColumnRenamed("LABEL", "Actor2Type1").drop('CODE')
    data=data.join(data_4,data.EventCode==data_4.CODE,how='left').withColumnRenamed("LABEL", "Event").drop('CODE')
    data=data.withColumn('EventDate', F.to_date(data.EventTimestamp))


    data=data.groupBy('EventDate','MonthYear','Year','EventCode','Event','Actor1CountryCode','Actor1Country'
    ,'Actor2CountryCode','Actor2Country','Actor1Type1Code','Actor1Type1','Actor2Type1Code','Actor2Type1').count().alias('EventsNum')
    
    data=data.withColumn('DaysPassed', F.datediff(F.current_date(),data.EventDate))
    data=data.toPandas()
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
