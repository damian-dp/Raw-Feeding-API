from flask import Blueprint, request, jsonify
from app import db
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('shopping_list', __name__, url_prefix='/shopping-list')

@bp.route('/', methods=['POST'])
@jwt_required()
def generate_shopping_list():
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    recipe_ids = request.json.get('recipe_ids', [])

    # Example request body:
    # {
    #     "recipe_ids": [1, 2, 3]
    # }

    if not recipe_ids:
        return jsonify({
            "error": "Missing data",
            "message": "No recipes provided. Please include at least one recipe ID in the 'recipe_ids' field."
        }), 400

    if not isinstance(recipe_ids, list) or not all(isinstance(id, int) for id in recipe_ids):
        return jsonify({
            "error": "Invalid data",
            "message": "The 'recipe_ids' field must be a list of integers."
        }), 400

    # Fetch recipes
    if current_user.is_admin:
        recipes = Recipe.query.filter(Recipe.id.in_(recipe_ids)).all()
    else:
        recipes = Recipe.query.filter(
            Recipe.id.in_(recipe_ids),
            ((Recipe.user_id == current_user_id) | (Recipe.is_public == True))
        ).all()

    if len(recipes) != len(recipe_ids):
        inaccessible_ids = set(recipe_ids) - set(recipe.id for recipe in recipes)
        return jsonify({
            "error": "Access denied",
            "message": "One or more recipes not found or not accessible.",
            "details": f"You don't have permission to access or the following recipe IDs do not exist: {list(inaccessible_ids)}"
        }), 403

    # Aggregate ingredients
    shopping_list = {}
    for recipe in recipes:
        for recipe_ingredient in recipe.ingredients:
            ingredient = recipe_ingredient.ingredient
            if ingredient.id in shopping_list:
                shopping_list[ingredient.id]['quantity'] += recipe_ingredient.quantity
            else:
                shopping_list[ingredient.id] = {
                    'name': ingredient.name,
                    'quantity': recipe_ingredient.quantity,
                    'unit': recipe_ingredient.unit
                }

    # Convert dictionary to list for JSON response
    shopping_list_result = [
        {
            'ingredient_id': ingredient_id,
            'name': item['name'],
            'quantity': item['quantity'],
            'unit': item['unit']
        }
        for ingredient_id, item in shopping_list.items()
    ]

    # Example successful response:
    # {
    #     "shopping_list": [
    #         {
    #             "ingredient_id": 1,
    #             "name": "Chicken Breast",
    #             "quantity": 1000,
    #             "unit": "grams"
    #         },
    #         {
    #             "ingredient_id": 2,
    #             "name": "Olive Oil",
    #             "quantity": 45,
    return jsonify(shopping_list_result), 200