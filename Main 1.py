from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_caching import Cache

#  Flask app
app = Flask(__name__)

# Configure the database URI for SQLAlchemy (using SQLite here)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'

# Initialize the SQLAlchemy object to handle database operations
db = SQLAlchemy(app)

# Models
class Document(db.Model):
    """Model representing a document stored in the database."""
    id = db.Column(db.Integer, primary_key=True)  
    content = db.Column(db.Text, nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
class User(db.Model):
    """Model representing a user and their query count to enforce rate limiting."""
    id = db.Column(db.Integer, primary_key=True) 
    query_count = db.Column(db.Integer, default=0)  

# Helper functions
def get_user_or_create(user_id):
    """Retrieve or create a new user with the given ID."""
    # Attempt to retrieve the user by ID
    user = User.query.get(user_id)
    
    # If the user doesn't exist, create a new user record with the provided user ID
    if not user:
        user = User(id=user_id, query_count=0)
        db.session.add(user)  # Adding new user 
        db.session.commit()  # Commit changes to the database
    return user

def increment_user_query_count(user):
    """Increment the user's query count and check the rate limit."""
    # If the user has made 5 or more queries, return a rate limit error
    if user.query_count >= 5:
        return jsonify({"error": "Too many requests"}), 429  # HTTP status code -  Too many requests
    
    # Increment the query count
    user.query_count += 1
    db.session.commit() 
    return None

# Routes
@app.before_first_request
def create_tables():
    """Create the database tables before the first request."""
    db.create_all()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint to verify if the API is active."""
    return jsonify({"status": "API is active"}), 200

@app.route('/search', methods=['GET'])
def search():
    """Search endpoint to retrieve documents containing the search text."""
    # Retrieve parameters from the request
    user_id = request.args.get('user_id') 
    search_text = request.args.get('text')  
    top_k = int(request.args.get('top_k', 5))  
    threshold = float(request.args.get('threshold', 0.5)) 

    # Check if the required parameters are present
    if not user_id or not search_text:
        return jsonify({"error": "Missing required parameters"}), 400  

    # Retrieve or create the user and enforce rate limiting
    user = get_user_or_create(user_id)
    rate_limit_error = increment_user_query_count(user)
    if rate_limit_error:
        return rate_limit_error 

    # Search for documents containing the search text
    documents = Document.query.filter(Document.content.contains(search_text)).limit(top_k).all()
    
    # Format the results to include document ID and content
    results = [{"doc_id": doc.id, "content": doc.content} for doc in documents]

    return jsonify(results), 200  # Return the search results as a JSON response

# Cache configuration
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
