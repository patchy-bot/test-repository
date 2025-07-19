# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Fixed SQL injection by replacing unsafe string interpolation with parameterized query using psycopg2's parameter substitution (%s). This properly escapes user input and prevents SQL injection attacks.

## Security Notes
Always use parameterized queries to handle user input in SQL statements. Avoid f-strings or string concatenation that directly inserts user input into SQL statements.

## Fixed Code
```py
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)
conn = psycopg2.connect(dbname='mydb', user='user', password='pass', host='localhost')
cursor = conn.cursor()

@app.route('/user/<username>')
def get_user(username):
    # Use parameterized query to prevent SQL injection
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user:
        return jsonify({'username': user[0], 'email': user[1]})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- import psycopg2

## Testing Recommendations
- Test normal and malicious username inputs to ensure no injection is possible.
- Verify correct data is returned for valid usernames.
- Confirm error returned for nonexistent users.

## Alternative Solutions
None provided
