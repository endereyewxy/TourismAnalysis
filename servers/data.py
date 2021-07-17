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
             '西藏',
             '香港',
             '澳门',
             '台湾']


class D:
    month_and_people = None

    relp_avg_cost = None

    relp_story_num = None

    play_way_percent_topn = None

    prov_hot = None

    spot_hot = None

    city_everypeolple_avg_cost = None

    quarter_days = None


def update_raw_database(database: str):
    spark = SparkSession.builder.config('spark.jars.packages', 'org.xerial:sqlite-jdbc:3.34.0').getOrCreate()

    loader = spark.read.format('jdbc')

    stories = loader.options(url='jdbc:sqlite:' + database, dbtable='stories', driver='org.sqlite.JDBC').load() \
        .filter(functions.col('view_count') >= 1000) \
        .filter(functions.col('like_count') != 0) \
        .withColumn('date_start', functions.split('date_start', r'/')) \
        .withColumn('date_start_y', functions.col('date_start')[0].cast('int')) \
        .withColumn('date_start_m', functions.col('date_start')[1].cast('int')) \
        .withColumn('date_start_d', functions.col('date_start')[2].cast('int')) \
        .withColumn('hot',
                    1 * functions.col('view_count') +
                    5 * functions.col('like_count') +
                    9 * functions.col('cmmt_count') +
                    2 * functions.col('pict_count'))
    scenics = loader.options(url='jdbc:sqlite:' + database, dbtable='scenics', driver='org.sqlite.JDBC').load()

    cities = loader.options(url='jdbc:sqlite:' + database, dbtable='cities', driver='org.sqlite.JDBC').load() \
        .withColumn('prov', functions \
                    .when(functions.col('name') == '北京', '北京') \
                    .when(functions.col('name') == '天津', '天津') \
                    .when(functions.col('name') == '重庆', '重庆') \
                    .when(functions.col('name') == '上海', '上海') \
                    .when(functions.col('name') == '香港', '香港') \
                    .when(functions.col('name') == '澳门', '澳门').otherwise(functions.col('prov')))
    visits = loader.options(url='jdbc:sqlite:' + database, dbtable='visits', driver='org.sqlite.JDBC').load()
    how_to = loader.options(url='jdbc:sqlite:' + database, dbtable='how_to', driver='org.sqlite.JDBC').load()

    D.month_and_people = stories.select('date_start_y', 'date_start_m') \
        .groupBy('date_start_y', 'date_start_m') \
        .count() \
        .orderBy(functions.col('date_start_m').asc()) \
        .collect()

    D.relp_avg_cost = stories.select('relp', 'cost', 'date_count') \
        .filter(functions.col('cost') <= 100000) \
        .withColumn('cost', stories.cost / stories.date_count) \
        .select('relp', 'cost') \
        .filter(functions.col('relp').isNotNull()) \
        .groupBy('relp') \
        .avg('cost') \
        .withColumnRenamed('avg(cost)', 'relp_avg_cost') \
        .collect()

    D.relp_story_num = stories.select('relp') \
        .groupBy('relp') \
        .count() \
        .withColumn('relp', functions.when(functions.col('relp').isNull(), '其他').otherwise(functions.col('relp'))) \
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

    D.prov_hot = visits.select('vstid', 'vctid') \
        .filter(functions.col('vctid').isNotNull()) \
        .join(stories, functions.col('vstid') == stories.stid, 'left') \
        .select('vctid', 'hot', 'date_start_y') \
        .filter(2019 <= functions.col('date_start_y')) \
        .filter(2021 >= functions.col('date_start_y')) \
        .join(cities, functions.col('vctid') == cities.ctid, 'left') \
        .select('prov', 'hot', 'date_start_y') \
        .filter(functions.col('prov').isin(provinces)) \
        .groupBy('date_start_y', 'prov') \
        .sum('hot') \
        .withColumnRenamed('date_start_y', 'year') \
        .withColumnRenamed('sum(hot)', 'hot') \
        .collect()

    D.spot_hot = visits.select('vstid', 'vscid') \
        .filter(functions.col('vscid').isNotNull()) \
        .join(stories, functions.col('vstid') == stories.stid, 'left') \
        .select('vscid', 'hot') \
        .join(scenics, functions.col('vscid') == scenics.scid, 'left') \
        .select('name', 'hot', 'lng', 'lat') \
        .groupBy('name', 'lng', 'lat') \
        .sum('hot') \
        .withColumnRenamed('sum(hot)', 'hot') \
        .limit(20) \
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
        .withColumn('avg(cost)', functions.bround(functions.col('avg(cost)'), scale=2)) \
        .collect()

    D.quarter_days = stories.select('date_count', 'date_start_m') \
        .withColumn('days', functions \
                    .when(functions.col('date_count') <= 3, 1) \
                    .when(functions.col('date_count') <= 7, 2) \
                    .when(functions.col('date_count') <= 10, 3) \
                    .when(functions.col('date_count') <= 15, 4).otherwise(5)) \
        .withColumn('quarter', functions \
                    .when(functions.col('date_start_m') <= 3, 0) \
                    .when(functions.col('date_start_m') <= 6, 1) \
                    .when(functions.col('date_start_m') <= 9, 2).otherwise(3)) \
        .select('days', 'quarter') \
        .groupBy('days', 'quarter') \
        .count() \
        .collect()

    spark.stop()
