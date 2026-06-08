"""Unit tests for Silver transforms. Uses a local Spark session —
no Databricks connection required."""

import pytest
from src.transforms.silver import (
    cap_uptime_pct,
    null_out_negative_resolution,
    null_out_of_range_nps,
    bucket_nps,
)


@pytest.fixture(scope="session")
def spark():
    from pyspark.sql import SparkSession
    return (
        SparkSession.builder.master("local[1]")
        .appName("silver-tests")
        .getOrCreate()
    )


def test_cap_uptime_caps_above_one(spark):
    df = spark.createDataFrame([(0.95,), (1.3,)], ["uptime_pct"])
    result = {r["uptime_pct"] for r in cap_uptime_pct(df).collect()}
    assert result == {0.95, 1.0}


def test_negative_resolution_becomes_null(spark):
    df = spark.createDataFrame([(5.0,), (-2.0,)], ["resolution_hours"])
    rows = null_out_negative_resolution(df).collect()
    values = sorted([r["resolution_hours"] for r in rows if r["resolution_hours"] is not None])
    nulls = sum(1 for r in rows if r["resolution_hours"] is None)
    assert values == [5.0] and nulls == 1


def test_nps_out_of_range_becomes_null(spark):
    df = spark.createDataFrame([(5,), (11,), (-1,)], ["nps_score"])
    nulls = sum(1 for r in null_out_of_range_nps(df).collect() if r["nps_score"] is None)
    assert nulls == 2  # 11 and -1 are invalid


def test_bucket_nps_classifies_correctly(spark):
    df = spark.createDataFrame([(3,), (7,), (10,)], ["nps_score"])
    buckets = [r["nps_bucket"] for r in bucket_nps(df).orderBy("nps_score").collect()]
    assert buckets == ["Detractor", "Passive", "Promoter"]
