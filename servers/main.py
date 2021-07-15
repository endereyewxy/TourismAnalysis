import operator
import random

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

if __name__ == '__main__':
    def foo(_):
        x = 2 * random.random() - 1
        y = 2 * random.random() - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0


    total = spark.sparkContext.parallelize(range(1, 2 * 10000 + 1), 2).map(foo).reduce(operator.add)
    print(0.0002 * total)

spark.stop()
