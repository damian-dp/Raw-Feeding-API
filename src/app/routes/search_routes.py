from flask import Blueprint, request, jsonify
from app.models.recipe import Recipe
from app.models.user import User
from app.models.ingredient import Ingredient
from ..schemas.recipe_schema import recipes_schema 
from ..schemas.ingredient_schema import ingredients_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.route_helpers import handle_errors

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/recipes', methods=['GET'])
@jwt_required()
@handle_errors
def search_recipes():
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    query = request.args.get('q', '')
    
    # Example request:
    # GET /search/recipes?q=chicken
    
    if not query:
        return jsonify({
            "error": "Invalid search",
            "message": "Please provide a search query using the 'q' parameter."
        }), 400

    if current_user.is_admin:
        recipes = Recipe.query.filter(
            Recipe.name.ilike(f'%{query}%') | Recipe.description.ilike(f'%{query}%')
        ).all()
    else:
        recipes = Recipe.query.filter(
            (Recipe.name.ilike(f'%{query}%') | Recipe.description.ilike(f'%{query}%')) &
            ((Recipe.user_id == current_user_id) | (Recipe.is_public == True))
        ).all()
    
    if not recipes:
        return jsonify({
            "message": "No recipes found",
            "details": "Your search did not match any recipes. Try different keywords or check your permissions."
        }), 404

    # Example successful response:
    # {
    #     "recipes": [
    #         {
    #             "id": 1,
    #             "name": "Grilled Chicken",
    #             "description": "Juicy grilled chicken breast",
    #             "instructions": "1. Marinate chicken...",
    #             "is_public": true,
    #             "user_id": 2,
    #             "ingredients": [
    #                 {
    #                     "id": 1,
    #                     "ingredient_id": 5,
    #                     "name": "Chicken Breast",
    #                     "quantity": 500,
    #                     "unit": "grams"
    #                 },
    #                 // ... more ingredients ...
    #             ]
    #         },
    #         // ... more recipes ...
    #     ]
    # }

    return recipes_schema.jsonify(recipes)

@bp.route('/ingredients', methods=['GET'])
def search_ingredients():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    # Example request:
    # GET /search/ingredients?q=tomato&category=vegetable
    
    ingredients_query = Ingredient.query.filter(Ingredient.name.ilike(f'%{query}%'))
    
    if category:
        ingredients_query = ingredients_query.filter(Ingredient.category == category)
    
    ingredients = ingredients_query.all()
    
    # Example successful response:
    # {
    #     "ingredients": [
    #         {
    #             "id": 1,
    #             "name": "Cherry Tomato",
    #             "category": "Vegetable",
    #             "calories": 18,
    #             "protein": 0.9,
    #             "fat": 0.2,
    #             "carbohydrates": 3.9
    #         },
    #         // ... more ingredients ...
    #     ]
    # }
    
    return ingredients_schema.jsonify(ingredients)

@bp.route('/recipes/by_ingredient', methods=['GET'])
@jwt_required()
def search_recipes_by_ingredient():
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    ingredient_id = request.args.get('ingredient_id')
    
    # Example request:
    # GET /search/recipes/by_ingredient?ingredient_id=5
    
    if not ingredient_id:
        return jsonify({
            "error": "Missing parameter",
            "message": "Ingredient ID is required. Please provide an 'ingredient_id' parameter in your request."
        }), 400
    
    try:
        ingredient_id = int(ingredient_id)
    except ValueError:
        return jsonify({
            "error": "Invalid parameter",
            "message": "The provided ingredient_id must be a valid integer."
        }), 400

    if current_user.is_admin:
        recipes = Recipe.query.join(Recipe.ingredients).filter(
            Recipe.ingredients.any(ingredient_id=ingredient_id)
        ).all()
    else:
        recipes = Recipe.query.join(Recipe.ingredients).filter(
            Recipe.ingredients.any(ingredient_id=ingredient_id) &
            ((Recipe.user_id == current_user_id) | (Recipe.is_public == True))
        ).all()
    
    if not recipes:
        return jsonify({
            "message": "No recipes found",
            "details": "No recipes were found with the specified ingredient. This could be because the ingredient doesn't exist, or you don't have permission to view recipes using this ingredient."
        }), 404

    # Example successful response:
    # {
    #     "recipes": [
    #         {
    #             "id": 1,
    #             "name": "Chicken Stir Fry",
    #             "description": "A quick and easy chicken stir fry recipe",
    #             "instructions": "1. Cut chicken into cubes...",
    #             "is_public": true,
    #             "user_id": 2,
    #             "ingredients": [
    #                 {
    #                     "id": 1,
    #                     "ingredient_id": 5,
    #                     "name": "Chicken Breast",
    #                     "quantity": 500,
    #                     "unit": "grams"
    #                 },
    #                 {
    #                     "id": 2,
    #                     "ingredient_id": 8,
    #                     "name": "Soy Sauce",
    #                     "quantity": 30,
    #                     "unit": "ml"
    #                 }
    #             ]
    #         },
    #         // ... more recipes ...
    #     ]
    # }

    return recipes_schema.jsonify(recipes)