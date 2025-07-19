from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.users_db

@app.route('/users/search', methods=['GET'])
def search_users():
    term = request.args.get('term', '')
    # Ensure term is a string and escape special regex chars
    import re
    safe_term = re.escape(term)
    # Use direct query on indexed fields instead of $where
    users = list(db.users.find({'name': {'$regex': safe_term, '$options': 'i'}}, {'_id': 0, 'name':1, 'email':1}))
    return jsonify(users)

if __name__ == '__main__':
    app.run()