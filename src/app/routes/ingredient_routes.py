from flask import Blueprint, jsonify
from app.models.ingredient import Ingredient
from ..schemas.ingredient_schema import ingredient_schema, ingredients_schema
from app.utils.route_helpers import handle_errors

bp = Blueprint('ingredients', __name__, url_prefix='/ingredients')

@bp.route('/', methods=['GET'])
@handle_errors
def get_ingredients():
    try:
        # Query to retrieve all ingredients from the database
        # This query fetches all Ingredient records without any filtering
        # It's used to provide a complete list of available ingredients
        # The query is executed lazily, meaning it only hits the database when the results are accessed
        ingredients = Ingredient.query.all()

        # Serialize the ingredients using the ingredients_schema
        # This converts the SQLAlchemy objects into a JSON-serializable format
        return ingredients_schema.jsonify(ingredients)
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@bp.route('/<int:ingredient_id>', methods=['GET'])
@handle_errors
def get_ingredient(ingredient_id):
    try:
        # Query to retrieve a specific ingredient by its ID
        # This query attempts to fetch a single Ingredient record using the provided ingredient_id
        # If no ingredient is found with the given ID, it automatically raises a 404 error
        # The get_or_404 method is used instead of get() to handle the case of a non-existent ingredient
        ingredient = Ingredient.query.get_or_404(ingredient_id)

        # Serialize the single ingredient using the ingredient_schema
        # This converts the SQLAlchemy object into a JSON-serializable format
        return ingredient_schema.jsonify(ingredient)
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500