import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = 'app.db'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Parameterized query to fetch stored hash
    cur.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Invalid credentials'}), 401
    user_id, stored_hash = row
    # Verify password using bcrypt
    import bcrypt
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return jsonify({'id': user_id, 'username': username})
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run()