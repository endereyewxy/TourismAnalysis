from pyspark.sql import SparkSession, functions

import settings


class D:
    month_avg_people = None

    relp_avg_cost = None


def update_raw_database(database: str):
    spark = SparkSession.builder.config('spark.jars.packages', 'org.xerial:sqlite-jdbc:3.34.0').getOrCreate()

    loader = spark.read.format('jdbc')

    stories = loader.options(url='jdbc:sqlite:' + database, dbtable='stories', driver='org.sqlite.JDBC').load() \
        .withColumn('date_start', functions.split('date_start', r'/'))
    scenics = loader.options(url='jdbc:sqlite:' + database, dbtable='scenics', driver='org.sqlite.JDBC').load()

    cities = loader.options(url='jdbc:sqlite:' + database, dbtable='cities', driver='org.sqlite.JDBC').load()
    visits = loader.options(url='jdbc:sqlite:' + database, dbtable='visits', driver='org.sqlite.JDBC').load()
    how_to = loader.options(url='jdbc:sqlite:' + database, dbtable='how_to', driver='org.sqlite.JDBC').load()

    stories = stories \
        .withColumn('date_start_y', stories.date_start[0].cast('int')) \
        .withColumn('date_start_m', stories.date_start[1].cast('int')) \
        .withColumn('date_start_d', stories.date_start[2].cast('int'))

    D.month_avg_people = stories.select('date_start_y', 'date_start_m') \
        .groupBy('date_start_y', 'date_start_m') \
        .count() \
        .groupBy('date_start_m') \
        .avg('count') \
        .withColumnRenamed('date_start_m', 'month') \
        .withColumnRenamed('avg(count)', 'people_num') \
        .collect()

    D.relp_avg_cost = stories.select('relp', 'cost', 'date_count') \
        .withColumn('cost', stories.cost / stories.date_count) \
        .select('relp', 'cost') \
        .groupBy('relp') \
        .avg('cost') \
        .withColumnRenamed('avg(cost)', 'avg_cost') \
        .collect()

    spark.stop()
