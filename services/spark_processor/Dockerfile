FROM bitnami/spark:3.4
USER root
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*
RUN pip install psycopg2-binary
ADD https://jdbc.postgresql.org/download/postgresql-42.5.0.jar /opt/spark/jars/
COPY wait_for_postgres.py processor.py /app/
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
