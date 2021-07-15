from pyspark.sql import SparkSession, functions


class D:
    month_avg_people = None

    relp_avg_cost = None

    relp_story_num = None

    play_way_percent_topn = None


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

    D.relp_story_num = stories.select('relp') \
        .groupBy('relp') \
        .count() \
        .withColumnRenamed('count', 'story_num') \
        .collect()

    D.play_way_percent_topn = how_to.select('h_tag') \
        .groupBy('h_tag') \
        .count() \
        .withColumnRenamed('h_tag', 'play_way') \
        .withColumnRenamed('count', 'percent')
    D.play_way_percent_topn = D.play_way_percent_topn \
        .withColumn('percent', functions.round(D.play_way_percent_topn.percent / stories.count() * 100).cast('int'))
    D.play_way_percent_topn = D.play_way_percent_topn \
        .orderBy(D.play_way_percent_topn.percent.desc()) \
        .collect()

    spark.stop()
