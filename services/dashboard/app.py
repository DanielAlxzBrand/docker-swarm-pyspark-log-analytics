import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )

@app.route('/stats', methods=['GET'])
def stats():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT page, total_views, unique_users, last_updated FROM page_stats ORDER BY total_views DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        'page': r[0],
        'total_views': r[1],
        'unique_users': r[2],
        'last_updated': r[3]
    } for r in rows])

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
