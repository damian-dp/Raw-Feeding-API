from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models.user import User
from ..schemas.user_schema import user_schema, users_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.utils.validators import validate_email, validate_password, validate_username
import sqlalchemy
from app.models.dog import Dog

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    is_admin = False

    if not validate_username(username):
        return jsonify({
            "error": "Invalid username. Username must be 3-20 characters long and contain only letters, numbers, and underscores."
        }), 400
    if not validate_email(email):
        return jsonify({
            "error": "Invalid email address. Please provide a valid email format."
        }), 400
    if not validate_password(password):
        return jsonify({
            "error": "Invalid password. Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
        }), 400

    try:
        new_user = current_app.auth_service.register_user(username, email, password)
        new_user.is_admin = is_admin
        db.session.commit()
        return user_schema.jsonify(new_user), 201
    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        if 'ix_user_email' in str(e):
            return jsonify({"error": "A user with this email already exists."}), 400
        elif 'ix_user_username' in str(e):
            return jsonify({"error": "A user with this username already exists."}), 400
        else:
            return jsonify({"error": "An error occurred while creating the user."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    
    include_dogs = request.args.get('include_dogs', 'false').lower() == 'true'
    include_recipes = request.args.get('include_recipes', 'false').lower() == 'true'
    
    if current_user.is_admin:
        users = User.query.all()
        result = users_schema.dump(users)
        for user, user_data in zip(users, result):
            if include_dogs:
                user_data['dog_ids'] = [dog.id for dog in user.dogs]
            if include_recipes:
                user_data['recipe_ids'] = [recipe.id for recipe in user.recipes]
        return jsonify(result)
    else:
        result = user_schema.dump(current_user)
        if include_dogs:
            result['dog_ids'] = [dog.id for dog in current_user.dogs]
        if include_recipes:
            result['recipe_ids'] = [recipe.id for recipe in current_user.recipes]
        return jsonify(result)

@bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    
    if current_user.is_admin or current_user.id == user_id:
        user = User.query.get_or_404(user_id)
        return user_schema.jsonify(user)
    else:
        return jsonify({"error": "Unauthorized. You can only view your own profile."}), 403

@bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    user_to_update = User.query.get_or_404(user_id)
    
    # Check if the current user is updating their own profile or is an admin
    if current_user.id != user_to_update.id and not current_user.is_admin:
        return jsonify({"error": "Unauthorized. You can only update your own profile."}), 403

    if 'username' in request.json:
        new_username = request.json['username']
        if not validate_username(new_username):
            return jsonify({
                "error": "Invalid username. Username must be 3-20 characters long and contain only letters, numbers, and underscores."
            }), 400
        user_to_update.username = new_username

    if 'email' in request.json:
        new_email = request.json['email']
        if not validate_email(new_email):
            return jsonify({
                "error": "Invalid email address. Please provide a valid email format."
            }), 400
        user_to_update.email = new_email

    if 'password' in request.json:
        new_password = request.json['password']
        if not validate_password(new_password):
            return jsonify({
                "error": "Invalid password. Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            }), 400
        user_to_update.set_password(new_password)

    # Only allow admins to update the is_admin field
    if 'is_admin' in request.json:
        if current_user.is_admin:
            user_to_update.is_admin = request.json['is_admin']
        else:
            return jsonify({"error": "Unauthorized. Only admins can update the admin status."}), 403

    db.session.commit()

    return user_schema.jsonify(user_to_update)

@bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    user_to_delete = User.query.get_or_404(user_id)
    
    # Check if the current user is deleting their own account or is an admin
    if current_user.id != user_to_delete.id and not current_user.is_admin:
        return jsonify({"error": "Unauthorized. You can only delete your own account."}), 403

    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200