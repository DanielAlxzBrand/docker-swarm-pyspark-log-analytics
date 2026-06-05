#!/bin/bash
python /app/wait_for_postgres.py
while true; do
    echo "Running PySpark processor at $(date)"
    spark-submit --master local[*] /app/processor.py
    echo "Sleeping for 5 minutes"
    sleep 300
done
