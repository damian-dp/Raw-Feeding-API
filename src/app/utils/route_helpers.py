from flask import jsonify, request
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from jwt.exceptions import PyJWTError
from marshmallow import ValidationError

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
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
        except SQLAlchemyError as e:
            return jsonify({"error": "Database error", "details": str(e)}), 500
        except PyJWTError as e:
            return jsonify({"error": "Authentication error", "details": str(e)}), 401
        except ValidationError as e:
            return jsonify({"error": "Validation error", "details": e.messages}), 400
        except ValueError as e:
            return jsonify({"error": "Invalid input", "details": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    return decorated_function

def validate_request_data(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if request.method in ['POST', 'PUT', 'PATCH']:
                    data = request.json
                else:
                    data = request.args
                validated_data = schema.load(data)
                return f(*args, **kwargs, validated_data=validated_data)
            except ValidationError as e:
                return jsonify({"error": "Validation error", "details": e.messages}), 400
        return decorated_function
    return decorator