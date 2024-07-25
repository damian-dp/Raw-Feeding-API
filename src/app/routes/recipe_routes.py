from flask import Blueprint, request, jsonify
from app import db
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from ..schemas.recipe_schema import recipe_schema, recipes_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.validators import (
    validate_recipe_name, validate_quantity, validate_ingredient_name, 
    validate_recipe_instructions, validate_recipe_description, validate_id_list,
    validate_unit, validate_is_public, validate_ingredient_id, validate_user_id,
    sanitize_string
)
from app.models.user import User
from app.models.dog import Dog
from app.models.ingredient import Ingredient
from app.utils.route_helpers import admin_required, handle_errors, validate_request_data

bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@bp.route('/', methods=['POST'])
@jwt_required()
@handle_errors
@validate_request_data(recipe_schema)
def create_recipe():
    user_id = get_jwt_identity()
    current_user = User.query.get_or_404(user_id)
    
    # Set the user_id in the validated data
    validated_data = request.json
    validated_data['user_id'] = user_id

    name = validated_data['name']
    description = validated_data.get('description')
    instructions = validated_data['instructions']
    is_public = validated_data.get('is_public', False)
    ingredients = validated_data['ingredients']
    dog_ids = validated_data.get('dog_ids', [])

    if not dog_ids:
        return jsonify({
            "error": "At least one dog must be associated with the recipe."
        }), 400

    if not validate_recipe_name(name):
        return jsonify({
            "error": "Invalid recipe name. Recipe name should be 3-100 characters long."
        }), 400

    if not validate_recipe_instructions(instructions):
        return jsonify({
            "error": "Invalid recipe instructions. Must be a non-empty string."
        }), 400

    if description and not validate_recipe_description(description):
        return jsonify({
            "error": "Invalid recipe description. Must be a string."
        }), 400

    if not validate_id_list(dog_ids):
        return jsonify({
            "error": "Invalid dog_ids. Must be a non-empty list of integers."
        }), 400

    if not validate_is_public(is_public):
        return jsonify({"error": "is_public must be a boolean value."}), 400

    for ingredient in ingredients:
        if not validate_ingredient_id(ingredient['ingredient_id']):
            return jsonify({"error": f"Invalid ingredient_id: {ingredient['ingredient_id']}. Must be a positive integer."}), 400
        if not validate_unit(ingredient['unit']):
            return jsonify({"error": f"Invalid unit for ingredient {ingredient['ingredient_id']}. Must be a non-empty string with max length 20."}), 400

    new_recipe = Recipe(name=name, description=description, instructions=instructions,
                        is_public=is_public, user_id=user_id)

    for ingredient in ingredients:
        ingredient_id = ingredient['ingredient_id']
        quantity = ingredient['quantity']
        unit = ingredient['unit']

        if not validate_quantity(quantity):
            return jsonify({
                "error": f"Invalid quantity for ingredient {ingredient_id}. Quantity must be a positive number."
            }), 400

        db_ingredient = Ingredient.query.get(ingredient_id)
        if not db_ingredient:
            return jsonify({
                "error": f"Ingredient with id {ingredient_id} not found. Please use a valid ingredient ID."
            }), 400
        
        if not validate_ingredient_name(db_ingredient.name):
            return jsonify({
                "error": f"Invalid ingredient name for id {ingredient_id}. Ingredient name should be 2-50 characters long and contain only letters, numbers, spaces, and hyphens."
            }), 400

        unit = sanitize_string(ingredient['unit'])
        recipe_ingredient = RecipeIngredient(
            ingredient_id=ingredient_id,
            quantity=quantity,
            unit=unit
        )
        new_recipe.ingredients.append(recipe_ingredient)

    for dog_id in dog_ids:
        dog = Dog.query.get(dog_id)
        if not dog:
            return jsonify({"error": f"Dog with id {dog_id} not found"}), 400
        if not current_user.is_admin and dog.user_id != user_id:
            return jsonify({"error": f"You don't have permission to assign dog with id {dog_id} to this recipe"}), 403
        new_recipe.dogs.append(dog)

    db.session.add(new_recipe)
    db.session.commit()

    return recipe_schema.jsonify(new_recipe), 201

@bp.route('/', methods=['GET'])
@jwt_required()
@handle_errors
def get_recipes():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get_or_404(current_user_id)

        if current_user.is_admin:
            recipes = Recipe.query.all()
        else:
            recipes = Recipe.query.filter((Recipe.user_id == current_user_id) | (Recipe.is_public == True)).all()

        return recipes_schema.jsonify(recipes)
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@bp.route('/<int:recipe_id>', methods=['GET'])
@jwt_required()
@handle_errors
def get_recipe(recipe_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    recipe = Recipe.query.get_or_404(recipe_id)

    if current_user.is_admin:
        return recipe_schema.jsonify(recipe)
    elif recipe.user_id == current_user_id or recipe.is_public:
        return recipe_schema.jsonify(recipe)
    else:
        return jsonify({
            "error": "Access denied",
            "message": "You do not have permission to view this recipe. You can only view your own recipes or public recipes."
        }), 403

@bp.route('/<int:recipe_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@handle_errors
@validate_request_data(recipe_schema)
def update_recipe(recipe_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    recipe = Recipe.query.get_or_404(recipe_id)

    if not current_user.is_admin and recipe.user_id != current_user_id:
        return jsonify({
            "error": "Access denied",
            "message": "You do not have permission to update this recipe. You can only update your own recipes."
        }), 403

    # Set the user_id in the validated data
    validated_data = request.json
    validated_data['user_id'] = current_user_id

    if 'name' in validated_data:
        new_name = validated_data['name']
        if not validate_recipe_name(new_name):
            return jsonify({
                "error": "Invalid recipe name. Recipe name should be 3-100 characters long."
            }), 400
        recipe.name = new_name

    if 'instructions' in validated_data:
        new_instructions = validated_data['instructions']
        if not validate_recipe_instructions(new_instructions):
            return jsonify({"error": "Invalid recipe instructions. Must be a non-empty string."}), 400
        recipe.instructions = new_instructions

    if 'description' in validated_data:
        new_description = validated_data['description']
        if not validate_recipe_description(new_description):
            return jsonify({"error": "Invalid recipe description. Must be a string."}), 400
        recipe.description = new_description

    if 'is_public' in validated_data:
        recipe.is_public = validated_data['is_public']

    if 'ingredients' in validated_data:
        # Remove existing ingredients
        recipe.ingredients = []
        # Add new ingredients
        for ingredient in validated_data['ingredients']:
            ingredient_id = ingredient['ingredient_id']
            quantity = ingredient['quantity']
            unit = ingredient['unit']

            if not validate_quantity(quantity):
                return jsonify({
                    "error": f"Invalid quantity for ingredient {ingredient_id}. Quantity must be a positive number."
                }), 400

            db_ingredient = Ingredient.query.get(ingredient_id)
            if not db_ingredient:
                return jsonify({
                    "error": f"Ingredient with id {ingredient_id} not found. Please use a valid ingredient ID."
                }), 400
            
            if not validate_ingredient_name(db_ingredient.name):
                return jsonify({
                    "error": f"Invalid ingredient name for id {ingredient_id}. Ingredient name should be 2-50 characters long and contain only letters, numbers, spaces, and hyphens."
                }), 400

            unit = sanitize_string(ingredient['unit'])
            recipe_ingredient = RecipeIngredient(
                ingredient_id=ingredient_id,
                quantity=quantity,
                unit=unit
            )
            recipe.ingredients.append(recipe_ingredient)

    if 'dog_ids' in validated_data:
        new_dog_ids = validated_data['dog_ids']
        if not validate_id_list(new_dog_ids):
            return jsonify({"error": "Invalid dog_ids. Must be a non-empty list of integers."}), 400
        # Remove existing dog associations
        recipe.dogs = []
        # Add new dog associations
        for dog_id in new_dog_ids:
            dog = Dog.query.get(dog_id)
            if not dog:
                return jsonify({"error": f"Dog with id {dog_id} not found"}), 400
            if not current_user.is_admin and dog.user_id != current_user_id:
                return jsonify({"error": f"You don't have permission to assign dog with id {dog_id} to this recipe"}), 403
            recipe.dogs.append(dog)
    # If no dog_ids are provided, keep the existing associations

    db.session.commit()

    # Refresh the recipe object to ensure all relationships are up-to-date
    db.session.refresh(recipe)

    return recipe_schema.jsonify(recipe), 200

@bp.route('/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
@handle_errors
def delete_recipe(recipe_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    recipe = Recipe.query.get_or_404(recipe_id)

    if not current_user.is_admin and recipe.user_id != current_user_id:
        return jsonify({
            "error": "Access denied",
            "message": "You do not have permission to delete this recipe. You can only delete your own recipes."
        }), 403

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({"message": "Recipe deleted successfully"}), 200