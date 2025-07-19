from flask import Flask, request, jsonify, session
import subprocess

app = Flask(__name__)
app.secret_key = 'replace_with_secure_random'

# Dummy authentication decorator
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({'error':'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    # Authenticate user (omitting real user store for brevity)
    session['user_id'] = 1
    return jsonify({'message':'Logged in'})

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.get_json() or {}
    src = data.get('from_account', '')
    dst = data.get('to_account', '')
    amt = data.get('amount', 0)
    # Validate inputs
    if not src.isdigit() or not dst.isdigit() or not isinstance(amt, (int, float)):
        return jsonify({'error':'Invalid parameters'}), 400
    # Perform transfer logic (placeholder)
    # subprocess call example (sanitized)
    cmd = ['bank_transfer', '--from', src, '--to', dst, '--amount', str(amt)]
    result = subprocess.run(cmd, shell=False, capture_output=True, text=True)
    if result.returncode != 0:
        return jsonify({'error': result.stderr}), 500
    return jsonify({'message':'Transfer successful'})

if __name__ == '__main__':
    app.run()