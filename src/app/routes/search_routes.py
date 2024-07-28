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
    # Query to retrieve the current user
    # This query fetches the User object for the authenticated user
    # If the user doesn't exist, it will raise a 404 error
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
        # Query to retrieve all recipes matching the search query for admin users
        # This query uses case-insensitive matching (ilike) on recipe name and description
        # It returns all matching recipes regardless of ownership or public status
        recipes = Recipe.query.filter(
            Recipe.name.ilike(f'%{query}%') | Recipe.description.ilike(f'%{query}%')
        ).all()
    else:
        # Query to retrieve recipes matching the search query for non-admin users
        # This query uses case-insensitive matching (ilike) on recipe name and description
        # It only returns recipes that are either owned by the current user or are public
        recipes = Recipe.query.filter(
            (Recipe.name.ilike(f'%{query}%') | Recipe.description.ilike(f'%{query}%')) &
            ((Recipe.user_id == current_user_id) | (Recipe.is_public == True))
        ).all()
    
    if not recipes:
        return jsonify({
            "message": "No recipes found",
            "details": "Your search did not match any recipes. Try different keywords or check your permissions."
        }), 404

    return recipes_schema.jsonify(recipes)

@bp.route('/ingredients', methods=['GET'])
@handle_errors
def search_ingredients():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    # Example request:
    # GET /search/ingredients?q=tomato&category=vegetable
    
    # Query to retrieve ingredients matching the search query
    # This query uses case-insensitive matching (ilike) on ingredient name
    ingredients_query = Ingredient.query.filter(Ingredient.name.ilike(f'%{query}%'))
    
    if category:
        # If a category is provided, further filter the query to match the category
        ingredients_query = ingredients_query.filter(Ingredient.category == category)
    
    # Execute the query and retrieve all matching ingredients
    ingredients = ingredients_query.all()
    
    return ingredients_schema.jsonify(ingredients)

@bp.route('/recipes/by_ingredient', methods=['GET'])
@jwt_required()
@handle_errors
def search_recipes_by_ingredient():
    current_user_id = get_jwt_identity()
    # Query to retrieve the current user
    # This query fetches the User object for the authenticated user
    # If the user doesn't exist, it will raise a 404 error
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
        # Query to retrieve all recipes containing the specified ingredient for admin users
        # This query joins the Recipe and RecipeIngredient tables and filters by ingredient_id
        # It returns all matching recipes regardless of ownership or public status
        recipes = Recipe.query.join(Recipe.ingredients).filter(
            Recipe.ingredients.any(ingredient_id=ingredient_id)
        ).all()
    else:
        # Query to retrieve recipes containing the specified ingredient for non-admin users
        # This query joins the Recipe and RecipeIngredient tables and filters by ingredient_id
        # It only returns recipes that are either owned by the current user or are public
        recipes = Recipe.query.join(Recipe.ingredients).filter(
            Recipe.ingredients.any(ingredient_id=ingredient_id) &
            ((Recipe.user_id == current_user_id) | (Recipe.is_public == True))
        ).all()
    
    if not recipes:
        return jsonify({
            "message": "No recipes found",
            "details": "No recipes were found with the specified ingredient. This could be because the ingredient doesn't exist, or you don't have permission to view recipes using this ingredient."
        }), 404

    return recipes_schema.jsonify(recipes)