from flask import jsonify, request
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get_or_404(current_user_id)
        if not current_user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    return decorated_function

def validate_request_data(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            errors = schema.validate(request.json)
            if errors:
                return jsonify({"error": "Validation error", "details": errors}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator