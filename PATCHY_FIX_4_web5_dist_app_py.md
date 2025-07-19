# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced string formatting of the SQL statement with a parameterized query using ? placeholders. Validated that 'id' is numeric before casting.

## Security Notes
Always use database parameter binding APIs instead of string interpolation. Validate incoming parameters for expected types.

## Fixed Code
```py
from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)
DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    if not user_id or not user_id.isdigit():
        abort(400, 'Invalid user id')
    conn = get_db()
    # Use parameterized query to prevent SQL injection
    cur = conn.execute('SELECT id, name, email FROM users WHERE id = ?', (int(user_id),))
    row = cur.fetchone()
    conn.close()
    if not row:
        abort(404, 'User not found')
    return jsonify(dict(row))

if __name__ == '__main__':
    app.run(debug=False)
```

## Additional Dependencies
None

## Testing Recommendations
- Pass valid and invalid ids
- Attempt SQL injection payloads in 'id' parameter
- Verify error messages don't leak SQL

## Alternative Solutions
None provided
