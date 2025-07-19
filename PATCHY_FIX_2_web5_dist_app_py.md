# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced unsafe string interpolation in the SQL query with a parameterized query using SQLite's parameter substitution ('?'). This prevents SQL injection by safely escaping user input before incorporating it into the SQL statement.

## Security Notes
Always use parameterized queries or prepared statements when executing SQL queries with user input. Avoid string concatenation or formatting with user-supplied data to mitigate SQL injection risks.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/user/<username>')
def get_user(username):
    # Use parameterized query to prevent SQL injection
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        return jsonify({'username': user[0], 'email': user[1]})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- import sqlite3

## Testing Recommendations
- Test with regular usernames returns correct data.
- Test with malicious input such as ' OR '1'='1 in username to confirm injection does not occur.
- Test user not found scenarios.

## Alternative Solutions
None provided
