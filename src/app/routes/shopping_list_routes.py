from flask import Blueprint, request, jsonify
from app.models.recipe import Recipe
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.route_helpers import handle_errors
from app.utils.validators import validate_user_id, validate_id_list, validate_ingredient_id, validate_quantity

bp = Blueprint('shopping_list', __name__, url_prefix='/shopping-list')

@bp.route('/', methods=['GET'])
@jwt_required()
@handle_errors
def get_shopping_list():
    try:
        current_user_id = get_jwt_identity()
        if not validate_user_id(current_user_id):
            return jsonify({"error": "Invalid user_id. Must be a positive integer."}), 400
        # Query to retrieve the current user
        # This query fetches the User object for the authenticated user
        # If the user doesn't exist, it will raise a 404 error
        current_user = User.query.get_or_404(current_user_id)
        recipe_ids = request.args.getlist('recipe_ids', type=int)

        if not recipe_ids:
            return jsonify({
                "error": "Missing data",
                "message": "No recipes provided. Please include at least one recipe ID in the 'recipe_ids' query parameter."
            }), 400

        if not validate_id_list(recipe_ids):
            return jsonify({
                "error": "Invalid recipe_ids. Must be a non-empty list of integers."
            }), 400

        # Fetch recipes
        if current_user.is_admin:
            # Query to retrieve all recipes with IDs in the recipe_ids list for admin users
            # This query uses the `in_` operator to match multiple IDs
            # It returns all matching recipes regardless of ownership or public status
            recipes = Recipe.query.filter(Recipe.id.in_(recipe_ids)).all()
        else:
            # Query to retrieve recipes for non-admin users
            # This query filters recipes based on three conditions:
            # 1. The recipe ID is in the provided recipe_ids list
            # 2. The recipe is owned by the current user OR
            # 3. The recipe is public
            # It ensures that users can only access their own recipes or public recipes
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
            # Iterate through the recipe_ingredient relationship
            # This accesses the 'ingredients' relationship of each Recipe object
            # It retrieves all RecipeIngredient objects associated with the recipe
            for recipe_ingredient in recipe.ingredients:
                # Access the Ingredient object through the RecipeIngredient relationship
                ingredient = recipe_ingredient.ingredient
                if not validate_ingredient_id(ingredient.id):
                    return jsonify({
                        "error": f"Invalid ingredient_id: {ingredient.id}. Must be a positive integer."
                    }), 400
                if ingredient.id in shopping_list:
                    new_quantity = shopping_list[ingredient.id]['quantity'] + recipe_ingredient.quantity
                    if not validate_quantity(new_quantity):
                        return jsonify({
                            "error": f"Invalid quantity for ingredient {ingredient.id}. Quantity must be a positive number."
                        }), 400
                    shopping_list[ingredient.id]['quantity'] = new_quantity
                else:
                    if not validate_quantity(recipe_ingredient.quantity):
                        return jsonify({
                            "error": f"Invalid quantity for ingredient {ingredient.id}. Quantity must be a positive number."
                        }), 400
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

        return jsonify(shopping_list_result), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500