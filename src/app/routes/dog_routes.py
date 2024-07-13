from flask import Blueprint, request, jsonify
from app import db
from app.models.dog import Dog
from app.schemas.dog_schema import dog_schema, dogs_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.validators import validate_date_of_birth, validate_weight
from app.models.user import User

bp = Blueprint('dogs', __name__, url_prefix='/dogs')

@bp.route('/', methods=['POST'])
@jwt_required()
def create_dog():
    user_id = get_jwt_identity()
    name = request.json['name']
    breed = request.json['breed']
    date_of_birth = request.json['date_of_birth']
    weight = request.json['weight']
    profile_image = request.json.get('profile_image')

    if not validate_date_of_birth(date_of_birth):
        return jsonify({
            "error": "Invalid date of birth. Please provide a date in the format YYYY-MM-DD and ensure it's not in the future."
        }), 400
    if not validate_weight(weight):
        return jsonify({
            "error": "Invalid weight. Weight must be a positive number less than 200 (assuming kg)."
        }), 400

    new_dog = Dog(name=name, breed=breed, date_of_birth=date_of_birth, 
                  weight=weight, profile_image=profile_image, user_id=user_id)

    db.session.add(new_dog)
    db.session.commit()

    return dog_schema.jsonify(new_dog), 201

@bp.route('/', methods=['GET'])
@jwt_required()
def get_dogs():
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    if current_user.is_admin:
        dogs = Dog.query.all()
    else:
        dogs = Dog.query.filter_by(user_id=current_user_id).all()

    return dogs_schema.jsonify(dogs)

@bp.route('/<int:dog_id>', methods=['GET'])
@jwt_required()
def get_dog(dog_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    dog = Dog.query.get_or_404(dog_id)

    if current_user.is_admin or dog.user_id == current_user_id:
        return dog_schema.jsonify(dog)
    else:
        return jsonify({
            "error": "Access denied",
            "message": "You do not have permission to view this dog. You can only view dogs that you own."
        }), 403

@bp.route('/<int:dog_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_dog(dog_id):
    user_id = get_jwt_identity()
    dog = Dog.query.filter_by(id=dog_id, user_id=user_id).first_or_404()

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
        new_date_of_birth = request.json['date_of_birth']
        if not validate_date_of_birth(new_date_of_birth):
            return jsonify({
                "error": "Invalid date of birth. Please provide a date in the format YYYY-MM-DD and ensure it's not in the future."
            }), 400
        dog.date_of_birth = new_date_of_birth

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

    return dog_schema.jsonify(dog)

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