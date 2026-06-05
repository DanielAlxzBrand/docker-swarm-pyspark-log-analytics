import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, countDistinct
import psycopg2
from datetime import datetime

def get_jdbc_url():
    return f"jdbc:postgresql://{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

def main():
    spark = SparkSession.builder \
        .appName("LogProcessor") \
        .config("spark.jars", "/opt/spark/jars/postgresql-42.5.0.jar") \
        .getOrCreate()

    jdbc_url = get_jdbc_url()
    properties = {
        "user": os.environ['DB_USER'],
        "password": os.environ['DB_PASSWORD'],
        "driver": "org.postgresql.Driver"
    }
    
    df = spark.read.jdbc(url=jdbc_url, table="raw_events", properties=properties)
    
    stats_df = df.groupBy("page").agg(
        count("*").alias("total_views"),
        countDistinct("user_id").alias("unique_users")
    )
    
    rows = stats_df.collect()
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    cur = conn.cursor()
    for row in rows:
        cur.execute("""
            INSERT INTO page_stats (page, total_views, unique_users, last_updated)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (page) DO UPDATE SET
                total_views = EXCLUDED.total_views,
                unique_users = EXCLUDED.unique_users,
                last_updated = EXCLUDED.last_updated
        """, (row.page, row.total_views, row.unique_users, datetime.utcnow()))
    conn.commit()
    cur.close()
    conn.close()
    
    spark.stop()
    print("PySpark job finished successfully")

if __name__ == '__main__':
    main()
