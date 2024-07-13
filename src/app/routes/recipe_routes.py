from flask import Blueprint, request, jsonify
from app import db
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from ..schemas.recipe_schema import recipe_schema, recipes_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.validators import validate_recipe_name, validate_quantity, validate_ingredient_name
from app.models.user import User

bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@bp.route('/', methods=['POST'])
@jwt_required()
def create_recipe():
    user_id = get_jwt_identity()
    name = request.json['name']
    description = request.json.get('description')
    instructions = request.json['instructions']
    is_public = request.json.get('is_public', False)
    ingredients = request.json['ingredients']

    if not validate_recipe_name(name):
        return jsonify({
            "error": "Invalid recipe name. Recipe name should be 3-100 characters long."
        }), 400

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

        recipe_ingredient = RecipeIngredient(
            ingredient_id=ingredient_id,
            quantity=quantity,
            unit=unit
        )
        new_recipe.ingredients.append(recipe_ingredient)

    db.session.add(new_recipe)
    db.session.commit()

    return recipe_schema.jsonify(new_recipe), 201

@bp.route('/', methods=['GET'])
@jwt_required()
def get_recipes():
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)

    if current_user.is_admin:
        recipes = Recipe.query.all()
    else:
        recipes = Recipe.query.filter((Recipe.user_id == current_user_id) | (Recipe.is_public == True)).all()

    return recipes_schema.jsonify(recipes)

@bp.route('/<int:recipe_id>', methods=['GET'])
@jwt_required()
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
def update_recipe(recipe_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    recipe = Recipe.query.get_or_404(recipe_id)

    if not current_user.is_admin and recipe.user_id != current_user_id:
        return jsonify({
            "error": "Access denied",
            "message": "You do not have permission to update this recipe. You can only update your own recipes."
        }), 403

    if 'name' in request.json:
        new_name = request.json['name']
        if not validate_recipe_name(new_name):
            return jsonify({
                "error": "Invalid recipe name. Recipe name should be 3-100 characters long."
            }), 400
        recipe.name = new_name

    recipe.description = request.json.get('description', recipe.description)
    recipe.instructions = request.json.get('instructions', recipe.instructions)
    recipe.is_public = request.json.get('is_public', recipe.is_public)

    if 'ingredients' in request.json:
        # Remove existing ingredients
        recipe.ingredients = []
        # Add new ingredients
        for ingredient in request.json['ingredients']:
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

            recipe_ingredient = RecipeIngredient(
                ingredient_id=ingredient_id,
                quantity=quantity,
                unit=unit
            )
            recipe.ingredients.append(recipe_ingredient)

    db.session.commit()

    return recipe_schema.jsonify(recipe)

@bp.route('/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
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