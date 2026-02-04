from flask import Flask, jsonify
import mysql.connector
import os
import socket

app = Flask(__name__)

DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_NAME = os.getenv('MYSQL_DATABASE')
DB_HOST = "db"
DB_USER = "root"

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route('/')
def home():
    container_id = socket.gethostname()
    return f"<h1>Hello from the Game-TDs App!</h1><p>Served by Container: <b>{container_id}</b></p>"

@app.route('/health')
def health_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({
            "status": "Success",
            "database": db_name[0],
            "container": socket.gethostname()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "Database Error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
