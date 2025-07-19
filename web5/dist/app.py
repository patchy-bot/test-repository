import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = 'app.db'

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cur.execute('SELECT id, username, email FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify({'id': row[0], 'username': row[1], 'email': row[2]})
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run()