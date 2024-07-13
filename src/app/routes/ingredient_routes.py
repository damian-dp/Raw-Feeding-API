from flask import Blueprint, jsonify
from app.models.ingredient import Ingredient
from app.schemas.ingredient_schema import ingredient_schema, ingredients_schema

bp = Blueprint('ingredients', __name__, url_prefix='/ingredients')

@bp.route('/', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    return ingredients_schema.jsonify(ingredients)

@bp.route('/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    return ingredient_schema.jsonify(ingredient)