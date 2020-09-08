# -*- coding:utf-8 -*-

#############################################################################

import subprocess as sub

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

from module.spark.settings import ELASTIC_PATH, ES_CONF

from util.fsUtils import Join, DirCheck, Delete
from util.hash import getSHA256

from common import getSharedPreferences
from webConfig import SHARED_PATH

from web.session import getSession
from webConfig import ES_URL

#############################################################################

sp                  = getSharedPreferences(SHARED_PATH)
ANALYSIS_DIR        = sp.getString('ANALYSIS_DIR')
SAMPLE_DIR        = sp.getString('SAMPLE_DIR')

SPARK_DIR           = Join(ANALYSIS_DIR, 'spark')
DUMP_PATH           = Join(SPARK_DIR, 'dump.csv')

sha256 = getSHA256(Join(SAMPLE_DIR, getSession('fileName')))

#############################################################################

spark = SparkSession                            \
        .builder                                \
        .master("local[8]")                     \
        .appName("strace parsing")              \
        .config("spark.jars", ELASTIC_PATH)     \
        .getOrCreate()

#############################################################################

df = spark.read.text(Join(SPARK_DIR, "strace.txt")).cache()
df = df.withColumnRenamed("value", "log")   \
        .select("log")                      \
        .coalesce(8)

#############################################################################

df = df.select( regexp_extract("log", r"^.+?\s{1}.+?\s{1}(.+?)\(.+", 1).alias("function"), "log")
print(f"ALL COUNT: {df.count()}")

#############################################################################

df = df.filter(~(df["function"].startswith("_")))               \
        .filter(~(df["function"].startswith("arena")))          \
        .filter(~(df["function"].startswith("je")))             \
        .filter(~(df["function"].startswith("j_")))             \
        .filter(~(df["function"].startswith("bin_")))           \
        .filter(~(df["function"].startswith("chunk_")))         \
        .filter(~(df["function"].startswith("pages_")))         \
        .filter(~(df["function"].contains("__")))               \
        .filter(~(df["function"].contains("mutex")))            \
        .filter(~(df["function"].contains("init")))             \
        .filter(~(df["function"].contains("free")))             \
        .filter(~(df["function"].contains("close")))            \
        .filter(~(df["function"].contains("sleep")))            \
        .filter(~(df["function"].contains("clock_gettime")))    \
        .filter(~(df["function"].contains("epoll_pwait")))      \


df = df.groupBy("function")                                     \
    .count()                                                    \
    .where(col("count") > 1)                                    \
    .orderBy(col("count").desc())                               \
    .withColumn("sha256", lit(sha256))

df.printSchema()
df.show(10, False)

#############################################################################

df.toPandas().to_csv(DUMP_PATH, sep=',', header=False, index=False)

cmd = f'curl -XDELETE "{ES_URL}/dynamic"'
sub.Popen(cmd).wait()

df.write                                                        \
    .format("org.elasticsearch.spark.sql")                      \
    .options(**ES_CONF)                                         \
    .option("es.resource", "dynamic/strace")                    \
    .mode("append")                                             \
    .save()

#############################################################################

spark.stop()

print("Spark done...")

#############################################################################
