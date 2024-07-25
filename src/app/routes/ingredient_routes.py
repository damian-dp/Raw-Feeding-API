from flask import Blueprint, jsonify
from app.models.ingredient import Ingredient
from ..schemas.ingredient_schema import ingredient_schema, ingredients_schema
from app.utils.route_helpers import handle_errors

bp = Blueprint('ingredients', __name__, url_prefix='/ingredients')

@bp.route('/', methods=['GET'])
@handle_errors
def get_ingredients():
    try:
        ingredients = Ingredient.query.all()
        return ingredients_schema.jsonify(ingredients)
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@bp.route('/<int:ingredient_id>', methods=['GET'])
@handle_errors
def get_ingredient(ingredient_id):
    try:
        ingredient = Ingredient.query.get_or_404(ingredient_id)
        return ingredient_schema.jsonify(ingredient)
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500