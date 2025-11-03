from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'flaskuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'flaskpw')
DB_NAME = os.environ.get('DB_NAME', 'flaskdb')
DB_PORT = int(os.environ.get('DB_PORT', 3306))

@app.route('/')
def index():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            connection_timeout=5
        )
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS visits (id INT AUTO_INCREMENT PRIMARY KEY, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
        cursor.execute('INSERT INTO visits () VALUES ()')
        conn.commit()
        cursor.execute('SELECT COUNT(*) FROM visits')
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({
            'status': 'ok',
            'db_host': DB_HOST,
            'visits': count
        })
    except Exception as e:
        return jsonify({'status': 'db_error', 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
