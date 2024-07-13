from flask import Blueprint, request, jsonify, current_app
from app.utils.validators import validate_username, validate_password

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not validate_username(username) or not validate_password(password):
        return jsonify({"error": "Invalid username or password"}), 400
    
    tokens = current_app.auth_service.authenticate_user(username, password)
    if tokens:
        return jsonify(tokens), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
