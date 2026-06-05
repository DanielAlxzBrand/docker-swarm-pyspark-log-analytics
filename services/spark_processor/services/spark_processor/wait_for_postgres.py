import time
import psycopg2
import os

def wait():
    while True:
        try:
            conn = psycopg2.connect(
                host=os.environ['DB_HOST'],
                port=os.environ['DB_PORT'],
                database=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD']
            )
            conn.close()
            print("PostgreSQL is ready")
            break
        except Exception as e:
            print("Waiting for postgres...", e)
            time.sleep(2)

if __name__ == '__main__':
    wait()
