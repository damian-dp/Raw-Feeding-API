from flask import Blueprint
from ..extensions import db
from ..models.ingredient import Ingredient

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_tables():
    ingredients = [
        Ingredient(name="Chicken Breast", category="Meat", calories=165, protein=31, fat=3.6, carbohydrates=0),
        Ingredient(name="Brown Rice", category="Grain", calories=216, protein=5, fat=1.8, carbohydrates=45),
        Ingredient(name="Broccoli", category="Vegetable", calories=55, protein=3.7, fat=0.6, carbohydrates=11.2),
        Ingredient(name="Salmon", category="Fish", calories=208, protein=20, fat=13, carbohydrates=0),
        Ingredient(name="Sweet Potato", category="Vegetable", calories=86, protein=1.6, fat=0.1, carbohydrates=20),
    ]

    db.session.add_all(ingredients)
    db.session.commit()
    print("Ingredients seeded")

@db_commands.cli.command("reset")
def reset_db():
    db.drop_all()
    db.create_all()
    seed_tables()
    print("Database reset and seeded")