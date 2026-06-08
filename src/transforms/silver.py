"""Silver-layer transformation functions, extracted from
01_bronze_silver_ingestion for unit testing."""

from pyspark.sql.functions import col, when


def cap_uptime_pct(df):
    """Cap uptime_pct values above 1.0 down to 1.0."""
    return df.withColumn(
        "uptime_pct",
        when(col("uptime_pct") > 1.0, 1.0).otherwise(col("uptime_pct")),
    )


def null_out_negative_resolution(df):
    """Replace negative resolution_hours with NULL (invalid data)."""
    return df.withColumn(
        "resolution_hours",
        when(col("resolution_hours") < 0, None).otherwise(col("resolution_hours")),
    )


def null_out_of_range_nps(df):
    """NPS scores must be 0-10; set out-of-range values to NULL."""
    return df.withColumn(
        "nps_score",
        when((col("nps_score") < 0) | (col("nps_score") > 10), None)
        .otherwise(col("nps_score")),
    )


def bucket_nps(df):
    """Classify nps_score into Detractor (0-6), Passive (7-8), Promoter (9-10)."""
    return df.withColumn(
        "nps_bucket",
        when(col("nps_score") <= 6, "Detractor")
        .when(col("nps_score") <= 8, "Passive")
        .when(col("nps_score") <= 10, "Promoter")
        .otherwise(None),
    )
