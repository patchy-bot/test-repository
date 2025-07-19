# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed use of $where entirely. We validate the input with a regex and then use a parameterized find() with $regex to do a case-insensitive exact match. No code execution in the database.

## Security Notes
Avoid $where or any JavaScript execution features in MongoDB when dealing with user input. Use built-in operators with sanitized values.

## Fixed Code
```py
from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
import re

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
users = db['users']

@app.route('/find', methods=['GET'])
def find_users():
    name_query = request.args.get('name')
    if not name_query or not re.fullmatch(r'[A-Za-z ]{1,50}', name_query):
        abort(400, 'Invalid name')
    # Use parameterized query without $where
    results = list(users.find({'name': {'$regex': f'^{re.escape(name_query)}$', '$options': 'i'}}, {'_id': 0}))
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False)
```

## Additional Dependencies
- import re

## Testing Recommendations
- Query existing and non-existing names
- Submit special regex characters to ensure they're escaped
- Audit logs to verify no $where use

## Alternative Solutions

### Use MongoDB Atlas search indexes
**Pros:** Rich search capabilities, No regex performance issues
**Cons:** Requires Atlas

