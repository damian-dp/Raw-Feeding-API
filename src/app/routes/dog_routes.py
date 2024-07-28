from flask import Blueprint, request, jsonify
from app import db
from app.models.dog import Dog
from ..schemas.dog_schema import dog_schema, dogs_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.validators import (
    validate_date_of_birth, validate_weight, validate_dog_name_or_breed, 
    validate_profile_image_url, validate_user_id, sanitize_string, validate_date_format, validate_url
)
from app.models.user import User
from datetime import datetime
from app.utils.route_helpers import handle_errors, validate_request_data

bp = Blueprint('dogs', __name__, url_prefix='/dogs')

@bp.route('/', methods=['POST'])
@jwt_required()
@handle_errors
def create_dog():
    try:
        user_id = get_jwt_identity()
        if not validate_user_id(user_id):
            return jsonify({"error": "Invalid user_id. Must be a positive integer."}), 400
        validated_data = request.json
        validated_data['user_id'] = user_id

        name = sanitize_string(validated_data['name'])
        breed = sanitize_string(validated_data['breed'])
        date_of_birth_input = validated_data['date_of_birth']
        weight = validated_data['weight']
        profile_image = validated_data.get('profile_image')

        if not validate_date_format(date_of_birth_input):
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        date_of_birth = datetime.strptime(date_of_birth_input, '%Y-%m-%d').date()

        is_valid_dob, dob_error = validate_date_of_birth(date_of_birth)
        if not is_valid_dob:
            return jsonify({"error": dob_error}), 400

        if not validate_weight(weight):
            return jsonify({
                "error": "Invalid weight. Weight must be a positive number less than 200 (assuming kg)."
            }), 400

        if not validate_dog_name_or_breed(name):
            return jsonify({"error": "Invalid dog name. Name must be 1-50 characters long."}), 400

        if not validate_dog_name_or_breed(breed):
            return jsonify({"error": "Invalid dog breed. Breed must be 1-50 characters long."}), 400

        if profile_image:
            if not validate_url(profile_image):
                return jsonify({"error": "Invalid profile image URL."}), 400
            if not validate_profile_image_url(profile_image):
                return jsonify({"error": "Invalid profile image URL. Must be a string with max length 255."}), 400

        # Create a new Dog instance and add it to the database
        # This query creates a new Dog record in the database with the provided attributes
        # It associates the dog with the current user and sets its initial properties
        new_dog = Dog(name=name, breed=breed, date_of_birth=date_of_birth, 
                      weight=weight, profile_image=profile_image, user_id=user_id)
        db.session.add(new_dog)
        db.session.commit()

        result = dog_schema.dump(new_dog)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@bp.route('/', methods=['GET'])
@jwt_required()
@handle_errors
def get_dogs():
    try:
        current_user_id = get_jwt_identity()
        # Query to retrieve the current user
        # This query fetches the User object for the authenticated user
        # It's used to determine the user's role (admin or regular user)
        current_user = User.query.get_or_404(current_user_id)

        # Query to retrieve dogs based on user role
        if current_user.is_admin:
            # For admin users, retrieve all dogs
            # This query fetches all Dog records from the database
            dogs = Dog.query.all()
            if not dogs:
                return jsonify({"message": "No dogs found. No user has created a dog yet."}), 404
        else:
            # For regular users, retrieve only their dogs
            # This query filters Dog records to only include those owned by the current user
            dogs = Dog.query.filter_by(user_id=current_user_id).all()
            if not dogs:
                return jsonify({"message": "No dogs found on your account. You haven't created any dogs yet."}), 404

        result = dogs_schema.dump(dogs)
        for dog, dog_data in zip(dogs, result):
            # Query to retrieve recipe IDs for each dog
            # This accesses the 'recipes' relationship of each Dog object
            # It retrieves the IDs of all recipes associated with the dog
            dog_data['recipes'] = [recipe.id for recipe in dog.recipes]

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@bp.route('/<int:dog_id>', methods=['GET'])
@jwt_required()
@handle_errors
def get_dog(dog_id):
    if not validate_user_id(dog_id):
        return jsonify({"error": "Invalid dog_id. Must be a positive integer."}), 400

    current_user_id = get_jwt_identity()
    # Query to retrieve the current user
    # This query fetches the User object for the authenticated user
    # It's used to check if the user is an admin or the owner of the requested dog
    current_user = User.query.get_or_404(current_user_id)
    
    # Query to retrieve the specific dog
    # This query fetches a single Dog record by its ID
    # If the dog doesn't exist, it will raise a 404 error
    dog = Dog.query.get_or_404(dog_id)

    if current_user.is_admin or dog.user_id == current_user_id:
        result = dog_schema.dump(dog)
        # Query to retrieve recipe IDs for the dog
        # This accesses the 'recipes' relationship of the Dog object
        # It retrieves the IDs of all recipes associated with the dog
        result['recipes'] = [recipe.id for recipe in dog.recipes]
        return jsonify(result)
    else:
        return jsonify({
            "error": "Access denied",
            "message": "You do not have permission to view this dog. You can only view dogs that you own."
        }), 403

@bp.route('/<int:dog_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@handle_errors
def update_dog(dog_id):
    if not validate_user_id(dog_id):
        return jsonify({"error": "Invalid dog_id. Must be a positive integer."}), 400

    current_user_id = get_jwt_identity()
    # Query to retrieve the current user
    # This query fetches the User object for the authenticated user
    # It's used to check if the user is an admin or the owner of the dog being updated
    current_user = User.query.get_or_404(current_user_id)
    
    # Query to retrieve the specific dog
    # This query fetches a single Dog record by its ID
    # If the dog doesn't exist, it will raise a 404 error
    dog = Dog.query.get_or_404(dog_id)

    if not current_user.is_admin and dog.user_id != current_user_id:
        return jsonify({
            "error": "Access denied",
            "message": "You do not have permission to update this dog. You can only update dogs that you own."
        }), 403

    validated_data = request.json
    validated_data['user_id'] = current_user_id

    if 'name' in validated_data:
        new_name = sanitize_string(validated_data['name'])
        if not validate_dog_name_or_breed(new_name):
            return jsonify({"error": "Invalid dog name. Name must be 1-50 characters long."}), 400
        dog.name = new_name

    if 'breed' in validated_data:
        new_breed = sanitize_string(validated_data['breed'])
        if not validate_dog_name_or_breed(new_breed):
            return jsonify({"error": "Invalid dog breed. Breed must be 1-50 characters long."}), 400
        dog.breed = new_breed

    if 'date_of_birth' in validated_data:
        date_of_birth_input = validated_data['date_of_birth']
        if not validate_date_format(date_of_birth_input):
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        date_of_birth = datetime.strptime(date_of_birth_input, '%Y-%m-%d').date()
        is_valid_dob, dob_error = validate_date_of_birth(date_of_birth)
        if not is_valid_dob:
            return jsonify({"error": dob_error}), 400
        dog.date_of_birth = date_of_birth

    if 'weight' in validated_data:
        new_weight = validated_data['weight']
        if not validate_weight(new_weight):
            return jsonify({
                "error": "Invalid weight. Weight must be a positive number less than 200 (assuming kg)."
            }), 400
        dog.weight = new_weight

    if 'profile_image' in validated_data:
        new_profile_image = validated_data['profile_image']
        if not validate_url(new_profile_image):
            return jsonify({"error": "Invalid profile image URL."}), 400
        if not validate_profile_image_url(new_profile_image):
            return jsonify({"error": "Invalid profile image URL. Must be a string with max length 255."}), 400
        dog.profile_image = new_profile_image

    # Commit the changes to the database
    # This operation saves all the changes made to the dog object
    # It updates the corresponding record in the database with the new values
    db.session.commit()

    return jsonify(dog_schema.dump(dog)), 200

@bp.route('/<int:dog_id>', methods=['DELETE'])
@jwt_required()
@handle_errors
def delete_dog(dog_id):
    if not validate_user_id(dog_id):
        return jsonify({"error": "Invalid dog_id. Must be a positive integer."}), 400

    current_user_id = get_jwt_identity()
    # Query to retrieve the current user
    # This query fetches the User object for the authenticated user
    # It's used to check if the user is an admin or the owner of the dog being deleted
    current_user = User.query.get_or_404(current_user_id)
    
    # Query to retrieve the specific dog
    # This query attempts to fetch a single Dog record by its ID
    # If the dog doesn't exist, it will return None
    dog = Dog.query.get(dog_id)
    if not dog:
        return jsonify({"error": "Dog not found", "message": "The specified dog does not exist or has already been deleted."}), 404

    if current_user.is_admin or dog.user_id == current_user_id:
        # Delete operation
        # This removes the dog object from the database session
        # The actual deletion from the database occurs when the session is committed
        db.session.delete(dog)
        # Commit the changes to the database
        # This operation permanently removes the dog record from the database
        db.session.commit()
        return jsonify({"msg": "Dog deleted"}), 200
    else:
        return jsonify({
            "error": "Access denied",
            "message": "You do not have permission to delete this dog. You can only delete dogs that you own."
        }), 403