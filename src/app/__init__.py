from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from marshmallow.exceptions import ValidationError
from .extensions import db, ma, jwt
from .models import User, Dog, Recipe, Ingredient, RecipeIngredient
import os

def create_app():
    app = Flask(__name__)
    
    try:
        # Load configuration
        app.config.from_object('config.Config')

        # Initialize extensions
        db.init_app(app)
        ma.init_app(app)
        jwt.init_app(app)

        # Import and register blueprints
        from .routes import user_routes, dog_routes, recipe_routes, ingredient_routes, shopping_list_routes, search_routes, auth_routes
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(dog_routes.bp)
        app.register_blueprint(recipe_routes.bp)
        app.register_blueprint(ingredient_routes.bp)
        app.register_blueprint(shopping_list_routes.bp)
        app.register_blueprint(search_routes.bp)
        app.register_blueprint(auth_routes.bp)
        
        # Register CLI commands
        from .controllers.cli_controller import db_commands
        app.register_blueprint(db_commands)

        # Error handlers
        @app.errorhandler(ValidationError)
        def validation_error(err):
            return jsonify({"error": err.messages}), 400

        @app.errorhandler(404)
        def not_found_error(error):
            return jsonify({"error": "Resource not found"}), 404

        @app.errorhandler(500)
        def internal_error(error):
            return jsonify({"error": "Internal server error"}), 500

        @app.errorhandler(Exception)
        def handle_exception(e):
            return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

        # Create AuthService instance
        from .services.AuthService import AuthService
        app.auth_service = AuthService()
        
        return app
    except Exception as e:
        print(f"An error occurred during app initialization: {str(e)}")
        return None