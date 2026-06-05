import os
import psycopg2
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )

@app.route('/event', methods=['POST'])
def create_event():
    data = request.get_json()
    page = data.get('page')
    user_id = data.get('user_id')
    if not page or not user_id:
        return jsonify({'error': 'page and user_id required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO raw_events (page, user_id, event_time) VALUES (%s, %s, %s)",
        (page, user_id, datetime.utcnow())
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'ok'}), 201

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)