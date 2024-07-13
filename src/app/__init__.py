from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from marshmallow.exceptions import ValidationError
from .extensions import db, ma, jwt
from .models import User, Dog, Recipe, Ingredient, RecipeIngredient

def create_app():
    app = Flask(__name__)
    
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

    # Error handler for ValidationError
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400

    # Create AuthService instance
    from .services.AuthService import AuthService
    auth_service = AuthService()
    app.auth_service = auth_service
    
    return app