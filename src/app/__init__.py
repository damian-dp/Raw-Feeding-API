from dotenv import load_dotenv
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow.exceptions import ValidationError

db = SQLAlchemy()
ma = Marshmallow()

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration settings
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)

    from .routes import user_routes, dog_routes, recipe_routes, ingredient_routes, shopping_list_routes, search_routes
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(dog_routes.bp)
    app.register_blueprint(recipe_routes.bp)
    app.register_blueprint(ingredient_routes.bp)
    app.register_blueprint(shopping_list_routes.bp)
    app.register_blueprint(search_routes.bp)
    
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400
    
    # Import the controllers
    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)
    
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)
    
    from controllers.card_controller import cards_bp
    app.register_blueprint(cards_bp)

    return app