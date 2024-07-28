from flask import Blueprint, request, jsonify, current_app
from app.utils.validators import validate_username, validate_password, validate_and_sanitize_email, sanitize_string, validate_is_admin
from app.utils.route_helpers import handle_errors, validate_request_data
from app import db
from ..schemas.user_schema import user_schema
import sqlalchemy

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
@handle_errors
def login():
    try:
        username = sanitize_string(request.json.get('username'))
        password = request.json.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        if not validate_username(username) or not validate_password(password):
            return jsonify({"error": "Invalid username or password format"}), 400

        # Authenticate user using the auth_service
        # This operation involves database queries to check the user's credentials
        # See AuthService.py for detailed comments on the database operations
        result, status_code = current_app.auth_service.authenticate_user(username, password)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

@bp.route('/register', methods=['POST'])
@handle_errors
def register():
    try:
        username = sanitize_string(request.json.get('username'))
        email, email_error = validate_and_sanitize_email(request.json.get('email'))
        if email_error:
            return jsonify({"error": f"Invalid email format: {email_error}"}), 400
        password = request.json.get('password')
        is_admin = request.json.get('is_admin', False)

        if not username or not email or not password:
            return jsonify({"error": "Username, email, and password are required"}), 400

        if not validate_username(username):
            return jsonify({"error": "Invalid username format"}), 400
        if not validate_password(password):
            return jsonify({"error": "Invalid password format"}), 400

        if not validate_is_admin(is_admin):
            return jsonify({"error": "Invalid is_admin value. Must be a boolean."}), 400

        # Register new user using the auth_service
        # This operation involves creating a new user record in the database
        # See AuthService.py for detailed comments on the database operations
        new_user, status_code = current_app.auth_service.register_user(username, email, password)
        if status_code != 201:
            return jsonify(new_user), status_code

        # Update the is_admin status of the new user
        # This modifies the user record in the database
        # See AuthService.py for detailed comments on the database operations
        new_user.is_admin = is_admin
        db.session.commit()

        return jsonify(user_schema.dump(new_user)), 201
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        # Handle database integrity errors (e.g., unique constraint violations)
        if 'ix_user_email' in str(e):
            return jsonify({"error": "A user with this email already exists."}), 400
        elif 'ix_user_username' in str(e):
            return jsonify({"error": "A user with this username already exists."}), 400
        else:
            return jsonify({"error": "An error occurred while creating the user."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500