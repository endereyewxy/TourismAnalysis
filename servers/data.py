from pyspark.sql import SparkSession, functions

provinces = ['四川',
             '浙江',
             '福建',
             '江苏',
             '湖南',
             '山东',
             '安徽',
             '广东',
             '河北',
             '湖北',
             '吉林',
             '上海',
             '江西',
             '广西',
             '贵州',
             '北京',
             '云南',
             '重庆',
             '河南',
             '陕西',
             '山西',
             '辽宁',
             '新疆',
             '内蒙古',
             '黑龙江',
             '天津',
             '甘肃',
             '海南',
             '青海',
             '宁夏',
             '西藏']


class D:
    month_avg_people = None

    relp_avg_cost = None

    relp_story_num = None

    play_way_percent_topn = None

    prov_hot = None

    city_everypeolple_avg_cost = None


def update_raw_database(database: str):
    spark = SparkSession.builder.config('spark.jars.packages', 'org.xerial:sqlite-jdbc:3.34.0').getOrCreate()

    loader = spark.read.format('jdbc')

    stories = loader.options(url='jdbc:sqlite:' + database, dbtable='stories', driver='org.sqlite.JDBC').load() \
        .withColumn('date_start', functions.split('date_start', r'/')) \
        .withColumn('date_start_y', functions.col('date_start')[0].cast('int')) \
        .withColumn('date_start_m', functions.col('date_start')[1].cast('int')) \
        .withColumn('date_start_d', functions.col('date_start')[2].cast('int')) \
        .withColumn('hot', functions.col('date_count') * functions.col('text_count'))
    scenics = loader.options(url='jdbc:sqlite:' + database, dbtable='scenics', driver='org.sqlite.JDBC').load()

    cities = loader.options(url='jdbc:sqlite:' + database, dbtable='cities', driver='org.sqlite.JDBC').load()
    visits = loader.options(url='jdbc:sqlite:' + database, dbtable='visits', driver='org.sqlite.JDBC').load()
    how_to = loader.options(url='jdbc:sqlite:' + database, dbtable='how_to', driver='org.sqlite.JDBC').load()

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
        .withColumnRenamed('relp', 'name') \
        .withColumnRenamed('count', 'value') \
        .collect()

    D.play_way_percent_topn = how_to.select('h_tag') \
        .groupBy('h_tag') \
        .count() \
        .withColumnRenamed('h_tag', 'play_way') \
        .withColumnRenamed('count', 'percent') \
        .withColumn('percent', functions.round(functions.col('percent') / stories.count() * 100).cast('int')) \
        .orderBy(functions.col('percent').desc()) \
        .collect()

    D.prov_hot = stories.select('date_start_y', 'loct', 'hot') \
        .filter(2019 <= functions.col('date_start_y')) \
        .filter(2021 >= functions.col('date_start_y')) \
        .join(cities, functions.col('loct') == cities.name) \
        .select('date_start_y', 'hot', 'prov') \
        .filter(functions.col('prov').isin(provinces)) \
        .groupBy('date_start_y', 'prov') \
        .sum('hot') \
        .withColumnRenamed('date_start_y', 'year') \
        .withColumnRenamed('sum(hot)', 'hot') \
        .collect()

    D.city_everypeolple_avg_cost = stories.select('date_start_y', 'loct', 'cost') \
        .filter(2019 <= functions.col('date_start_y')) \
        .filter(2021 >= functions.col('date_start_y')) \
        .join(cities, functions.col('loct') == cities.name) \
        .select('date_start_y', 'prov', 'cost') \
        .filter(functions.col('prov').isin(provinces)) \
        .groupBy('date_start_y', 'prov') \
        .avg('cost') \
        .withColumnRenamed('date_start_y', 'year') \
        .orderBy(functions.col('avg(cost)').desc()) \
        .collect()

    spark.stop()
