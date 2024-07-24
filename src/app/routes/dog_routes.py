from flask import Blueprint, request, jsonify
from app import db
from app.models.dog import Dog
from ..schemas.dog_schema import dog_schema, dogs_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.validators import validate_date_of_birth, validate_weight
from app.models.user import User
from app.models.recipe import Recipe
from datetime import datetime

bp = Blueprint('dogs', __name__, url_prefix='/dogs')

@bp.route('/', methods=['POST'])
@jwt_required()
def create_dog():
    try:
        user_id = get_jwt_identity()
        name = request.json['name']
        breed = request.json['breed']
        date_of_birth_input = request.json['date_of_birth']
        weight = request.json['weight']
        profile_image = request.json.get('profile_image')

        # Handle date_of_birth input
        if isinstance(date_of_birth_input, str):
            date_of_birth = datetime.strptime(date_of_birth_input, '%Y-%m-%d').date()
        elif isinstance(date_of_birth_input, datetime):
            date_of_birth = date_of_birth_input.date()
        else:
            date_of_birth = date_of_birth_input

        is_valid_dob, dob_error = validate_date_of_birth(date_of_birth)
        if not is_valid_dob:
            return jsonify({"error": dob_error}), 400

        if not validate_weight(weight):
            return jsonify({
                "error": "Invalid weight. Weight must be a positive number less than 200 (assuming kg)."
            }), 400

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
def get_dogs():
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    if current_user.is_admin:
        dogs = Dog.query.all()
    else:
        dogs = Dog.query.filter_by(user_id=current_user_id).all()

    result = dogs_schema.dump(dogs)
    for dog, dog_data in zip(dogs, result):
        dog_data['recipes'] = [recipe.id for recipe in dog.recipes]

    return jsonify(result)

@bp.route('/<int:dog_id>', methods=['GET'])
@jwt_required()
def get_dog(dog_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    dog = Dog.query.get_or_404(dog_id)

    if current_user.is_admin or dog.user_id == current_user_id:
        result = dog_schema.dump(dog)
        result['recipes'] = [recipe.id for recipe in dog.recipes]
        return jsonify(result)
    else:
        return jsonify({
            "error": "Access denied",
            "message": "You do not have permission to view this dog. You can only view dogs that you own."
        }), 403

@bp.route('/<int:dog_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_dog(dog_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    dog = Dog.query.get_or_404(dog_id)

    if not current_user.is_admin and dog.user_id != current_user_id:
        return jsonify({
            "error": "Access denied",
            "message": "You do not have permission to update this dog. You can only update dogs that you own."
        }), 403

    if 'name' in request.json:
        new_name = request.json['name']
        if not new_name or len(new_name) > 50:
            return jsonify({
                "error": "Invalid dog name. Name must be 1-50 characters long."
            }), 400
        dog.name = new_name

    if 'breed' in request.json:
        new_breed = request.json['breed']
        if not new_breed or len(new_breed) > 50:
            return jsonify({
                "error": "Invalid dog breed. Breed must be 1-50 characters long."
            }), 400
        dog.breed = new_breed

    if 'date_of_birth' in request.json:
        date_of_birth_input = request.json['date_of_birth']
        if isinstance(date_of_birth_input, str):
            date_of_birth = datetime.strptime(date_of_birth_input, '%Y-%m-%d').date()
        elif isinstance(date_of_birth_input, datetime):
            date_of_birth = date_of_birth_input.date()
        else:
            date_of_birth = date_of_birth_input
        is_valid_dob, dob_error = validate_date_of_birth(date_of_birth)
        if not is_valid_dob:
            return jsonify({"error": dob_error}), 400
        dog.date_of_birth = date_of_birth

    if 'weight' in request.json:
        new_weight = request.json['weight']
        if not validate_weight(new_weight):
            return jsonify({
                "error": "Invalid weight. Weight must be a positive number less than 200 (assuming kg)."
            }), 400
        dog.weight = new_weight

    if 'profile_image' in request.json:
        dog.profile_image = request.json['profile_image']

    db.session.commit()

    return dog_schema.jsonify(dog), 200

@bp.route('/<int:dog_id>', methods=['DELETE'])
@jwt_required()
def delete_dog(dog_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    dog = Dog.query.get_or_404(dog_id)

    if current_user.is_admin or dog.user_id == current_user_id:
        db.session.delete(dog)
        db.session.commit()
        return jsonify({"msg": "Dog deleted"}), 200
    else:
        return jsonify({
            "error": "Access denied",
            "message": "You do not have permission to delete this dog. You can only delete dogs that you own."
        }), 403