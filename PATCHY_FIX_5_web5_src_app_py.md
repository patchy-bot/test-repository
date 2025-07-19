# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Changed SQL to use parameterized placeholders. Validated 'username' type. Wildcard search done securely by binding the pattern.

## Security Notes
Never concatenate user input into SQL. Parameterized queries protect against injection. Sanitize and validate types.

## Fixed Code
```py
from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)
DB_PATH = 'users.db'

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search', methods=['POST'])
def search_user():
    data = request.json or {}
    username = data.get('username')
    if not isinstance(username, str) or not username:
        abort(400, 'Invalid username')
    conn = connect_db()
    # Use parameterized query with wildcard
    cur = conn.execute('SELECT id, name FROM users WHERE name LIKE ?', (f"%{username}%",))
    users = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=False)
```

## Additional Dependencies
None

## Testing Recommendations
- Search common names
- Attempt injection payloads
- Check empty and special-character usernames

## Alternative Solutions
None provided
