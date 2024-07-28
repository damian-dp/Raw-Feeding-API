from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from ..schemas.user_schema import user_schema, users_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.validators import validate_password, validate_username, validate_user_id, sanitize_string, validate_is_admin, validate_and_sanitize_email, validate_url
from app.utils.route_helpers import handle_errors, validate_request_data

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/', methods=['GET'])
@jwt_required()
@handle_errors
def get_users():
    try:
        current_user_id = get_jwt_identity()
        # Query to retrieve the current user
        # This query fetches the User object for the authenticated user
        # If the user doesn't exist, it will raise a 404 error
        current_user = User.query.get_or_404(current_user_id)
        
        include_dogs = request.args.get('include_dogs', 'false').lower() == 'true'
        include_recipes = request.args.get('include_recipes', 'false').lower() == 'true'
        
        if current_user.is_admin:
            # Query to retrieve all users
            # This query fetches all User objects from the database
            # It's only executed for admin users to get a list of all users
            users = User.query.all()
            result = users_schema.dump(users)
            for user, user_data in zip(users, result):
                if include_dogs:
                    # Access the 'dogs' relationship of each User object
                    # This retrieves all Dog objects associated with the user
                    user_data['dog_ids'] = [dog.id for dog in user.dogs]
                if include_recipes:
                    # Access the 'recipes' relationship of each User object
                    # This retrieves all Recipe objects associated with the user
                    user_data['recipe_ids'] = [recipe.id for recipe in user.recipes]
            return jsonify(result)
        else:
            # For non-admin users, only return their own user data
            result = user_schema.dump(current_user)
            if include_dogs:
                # Access the 'dogs' relationship of the current User object
                # This retrieves all Dog objects associated with the current user
                result['dog_ids'] = [dog.id for dog in current_user.dogs]
            if include_recipes:
                # Access the 'recipes' relationship of the current User object
                # This retrieves all Recipe objects associated with the current user
                result['recipe_ids'] = [recipe.id for recipe in current_user.recipes]
            return jsonify(result)
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@handle_errors
def get_user(user_id):
    current_user_id = get_jwt_identity()
    # Query to retrieve the current user
    # This query fetches the User object for the authenticated user
    # If the user doesn't exist, it will raise a 404 error
    current_user = User.query.get_or_404(current_user_id)
    
    if not validate_user_id(user_id):
        return jsonify({"error": "Invalid user_id. Must be a positive integer."}), 400
    
    include_dogs = request.args.get('include_dogs', 'false').lower() == 'true'
    include_recipes = request.args.get('include_recipes', 'false').lower() == 'true'
    
    if current_user.is_admin or current_user.id == user_id:
        # Query to retrieve the requested user
        # This query fetches the User object for the specified user_id
        # If the user doesn't exist, it will raise a 404 error
        user = User.query.get_or_404(user_id)
        result = user_schema.dump(user)
        if include_dogs:
            # Access the 'dogs' relationship of the User object
            # This retrieves all Dog objects associated with the user
            result['dog_ids'] = [dog.id for dog in user.dogs]
        if include_recipes:
            # Access the 'recipes' relationship of the User object
            # This retrieves all Recipe objects associated with the user
            result['recipe_ids'] = [recipe.id for recipe in user.recipes]
        return jsonify(result)
    else:
        return jsonify({"error": "Unauthorized. You can only view your own profile."}), 403

@bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@handle_errors
def update_user(user_id):
    current_user_id = get_jwt_identity()
    # Query to retrieve the current user
    # This query fetches the User object for the authenticated user
    # If the user doesn't exist, it will raise a 404 error
    current_user = User.query.get_or_404(current_user_id)
    # Query to retrieve the user to be updated
    # This query fetches the User object for the specified user_id
    # If the user doesn't exist, it will raise a 404 error
    user_to_update = User.query.get_or_404(user_id)
    
    if not validate_user_id(user_id):
        return jsonify({"error": "Invalid user_id. Must be a positive integer."}), 400
    
    if current_user.id != user_to_update.id and not current_user.is_admin:
        return jsonify({"error": "Unauthorized. You can only update your own profile."}), 403

    validated_data = request.json
    validated_data['user_id'] = current_user_id

    if 'username' in validated_data:
        new_username = sanitize_string(validated_data['username'])
        if not validate_username(new_username):
            return jsonify({
                "error": "Invalid username. Username must be 3-20 characters long and contain only letters, numbers, and underscores."
            }), 400
        user_to_update.username = new_username

    if 'email' in validated_data:
        new_email, error = validate_and_sanitize_email(validated_data['email'])
        if error:
            return jsonify({"error": f"Invalid email address: {error}"}), 400
        user_to_update.email = new_email

    if 'password' in validated_data:
        new_password = validated_data['password']
        if not validate_password(new_password):
            return jsonify({
                "error": "Invalid password. Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            }), 400
        user_to_update.set_password(new_password)

    if 'is_admin' in validated_data:
        if current_user.is_admin:
            if not validate_is_admin(validated_data['is_admin']):
                return jsonify({"error": "Invalid is_admin value. Must be a boolean."}), 400
            user_to_update.is_admin = validated_data['is_admin']
        else:
            return jsonify({"error": "Unauthorized. Only admins can update the admin status."}), 403

    if 'profile_picture_url' in validated_data:
        if not validate_url(validated_data['profile_picture_url']):
            return jsonify({"error": "Invalid URL for profile picture."}), 400
        user_to_update.profile_picture_url = validated_data['profile_picture_url']

    # Commit the changes to the database
    # This saves all the modifications to the user_to_update object
    db.session.commit()

    return jsonify(user_schema.dump(user_to_update))

@bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@handle_errors
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    # Query to retrieve the current user
    # This query fetches the User object for the authenticated user
    # If the user doesn't exist, it will raise a 404 error
    current_user = User.query.get_or_404(current_user_id)
    # Query to retrieve the user to be deleted
    # This query fetches the User object for the specified user_id
    # If the user doesn't exist, it will raise a 404 error
    user_to_delete = User.query.get_or_404(user_id)
    
    if not validate_user_id(user_id):
        return jsonify({"error": "Invalid user_id. Must be a positive integer."}), 400
    
    if current_user.id != user_to_delete.id and not current_user.is_admin:
        return jsonify({"error": "Unauthorized. You can only delete your own account."}), 403

    # Delete the user from the database
    # This removes the user and all associated data (due to cascade delete settings)
    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200