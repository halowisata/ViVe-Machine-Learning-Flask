# routes/api.py

from flask import Blueprint, jsonify

# Create a Blueprint object for the API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Define API endpoints
@api_bp.route('/users')
def get_users():
    users = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
    return jsonify(users)

@api_bp.route('/users/<int:user_id>')
def get_user(user_id):
    user = {'id': user_id, 'name': 'John'}
    return jsonify(user)
