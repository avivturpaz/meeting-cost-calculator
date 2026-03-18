import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY', 'dev-secret-key')

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

PADDLE_API_KEY = os.environ.get('PADDLE_API_KEY', '')
PADDLE_PRICE_ID = os.environ.get('PADDLE_PRICE_ID', '')
PADDLE_SANDBOX = os.environ.get('PADDLE_SANDBOX', 'true').lower() == 'true'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        people INTEGER,
        hourly_rate REAL,
        duration_seconds INTEGER,
        total_cost REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html',
                           paddle_sandbox=PADDLE_SANDBOX,
                           paddle_price_id=PADDLE_PRICE_ID)


@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/save-session', methods=['POST'])
def save_session():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO sessions (people, hourly_rate, duration_seconds, total_cost) VALUES (?, ?, ?, ?)',
              (data.get('people'), data.get('hourly_rate'), data.get('duration_seconds'), data.get('total_cost')))
    conn.commit()
    conn.close()
    return jsonify({'status': 'saved'}), 200


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/cancel')
def cancel():
    return render_template('cancel.html')


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


init_db()
