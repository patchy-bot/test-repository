# Security Fix for web3/param/app.py

**Vulnerability Type:** COMMAND_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** Yes

## Original Issue
Added session-based authentication and a login_required decorator. Removed os.system and replaced with internal logic stub. Validated 'account' with a regex allowlist and 'amount' parsed as float.

## Security Notes
Always authenticate sensitive operations. Avoid shell commands by using internal functions or subprocess with shell=False. Validate all inputs via allowlists.

## Fixed Code
```py
from flask import Flask, request, jsonify, abort, session
from functools import wraps
import subprocess
import re

app = Flask(__name__)
app.secret_key = 'REPLACE_WITH_SECURE_RANDOM'

# Simple login_required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            abort(401, 'Authentication required')
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    # Stub example: in production, validate against user store
    user = request.json.get('username')
    pwd = request.json.get('password')
    if user == 'alice' and pwd == 'secret':
        session['user_id'] = user
        return jsonify({'message':'logged in'})
    abort(401, 'Invalid credentials')

@app.route('/transfer', methods=['POST'])
@login_required
def transfer_money():
    data = request.json
    target = data.get('account')
    amount = data.get('amount')
    # Validate account identifier (allow only alphanumerics)
    if not re.fullmatch(r'[A-Za-z0-9]+', target):
        abort(400, 'Invalid account format')
    # Validate amount is positive decimal
    try:
        amount_val = float(amount)
        if amount_val <= 0:
            raise ValueError()
    except:
        abort(400, 'Invalid amount')
    # Perform transfer logic safely instead of shell command
    # e.g., call internal function or microservice
    # Example stub response:
    return jsonify({'from': session['user_id'], 'to': target, 'amount': amount_val})

if __name__ == '__main__':
    app.run(debug=False)
```

## Additional Dependencies
- import re
- from functools import wraps

## Testing Recommendations
- Attempt transfer without login (should 401)
- Try invalid account strings and negative amounts
- Ensure session cookie is HttpOnly and Secure

## Alternative Solutions

### Use OAuth or JWT tokens for authentication
**Pros:** Stateless, Wider ecosystem
**Cons:** More setup complexity

