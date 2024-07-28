from flask import Blueprint
from ..extensions import db
from ..models.ingredient import Ingredient
from ..models import User, Dog, Recipe, Ingredient, RecipeIngredient
from sqlalchemy.exc import SQLAlchemyError

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    try:
        db.create_all()
        print("Tables created successfully")
    except SQLAlchemyError as e:
        print(f"An error occurred while creating tables: {str(e)}")

@db_commands.cli.command("drop")
def drop_tables():
    try:
        db.drop_all()
        print("Tables dropped successfully")
    except SQLAlchemyError as e:
        print(f"An error occurred while dropping tables: {str(e)}")

@db_commands.cli.command("seed")
def seed_tables():
    try:
        # Seed admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('12345678Aa@')  # Use a secure password in production
        db.session.add(admin)
        db.session.commit()
        print("Admin user seeded successfully")

        # Seed ingredients
        ingredients = [
            Ingredient(name="Chicken Breast", category="Meat", calories=165, protein=31, fat=3.6, carbohydrates=0),
            Ingredient(name="Brown Rice", category="Grain", calories=216, protein=5, fat=1.8, carbohydrates=45),
            Ingredient(name="Broccoli", category="Vegetable", calories=55, protein=3.7, fat=0.6, carbohydrates=11.2),
            Ingredient(name="Salmon", category="Fish", calories=208, protein=20, fat=13, carbohydrates=0),
            Ingredient(name="Sweet Potato", category="Vegetable", calories=86, protein=1.6, fat=0.1, carbohydrates=20),
            Ingredient(name="Beef Liver", category="Organ Meat", calories=135, protein=20.4, fat=3.6, carbohydrates=3.9),
            Ingredient(name="Turkey", category="Meat", calories=189, protein=29, fat=7.5, carbohydrates=0),
            Ingredient(name="Pumpkin", category="Vegetable", calories=26, protein=1, fat=0.1, carbohydrates=6),
            Ingredient(name="Eggs", category="Protein", calories=143, protein=12.6, fat=9.5, carbohydrates=0.7),
            Ingredient(name="Green Beans", category="Vegetable", calories=31, protein=1.8, fat=0.2, carbohydrates=7),
            Ingredient(name="Lamb", category="Meat", calories=294, protein=25, fat=21, carbohydrates=0),
            Ingredient(name="Chicken Heart", category="Organ Meat", calories=185, protein=26, fat=8.5, carbohydrates=0),
            Ingredient(name="Quinoa", category="Grain", calories=120, protein=4.4, fat=1.9, carbohydrates=21),
            Ingredient(name="Blueberries", category="Fruit", calories=57, protein=0.7, fat=0.3, carbohydrates=14),
            Ingredient(name="Beef Kidney", category="Organ Meat", calories=131, protein=22.6, fat=3.1, carbohydrates=1.8),
            Ingredient(name="Sardines", category="Fish", calories=208, protein=24.6, fat=11.5, carbohydrates=0),
            Ingredient(name="Spinach", category="Vegetable", calories=23, protein=2.9, fat=0.4, carbohydrates=3.6),
            Ingredient(name="Duck", category="Meat", calories=337, protein=19, fat=28.4, carbohydrates=0),
            Ingredient(name="Carrots", category="Vegetable", calories=41, protein=0.9, fat=0.2, carbohydrates=9.6),
            Ingredient(name="Beef Tripe", category="Organ Meat", calories=85, protein=12, fat=3.5, carbohydrates=0),
        ]

        db.session.add_all(ingredients)
        db.session.commit()
        print("Ingredients seeded successfully")

        # Check if admin user exists
        admin_check = User.query.filter_by(username='admin').first()
        if admin_check:
            print(f"Admin user found: {admin_check.username}, {admin_check.email}")
        else:
            print("Admin user not found in the database")

        print("Database seeded successfully")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"An error occurred during seeding: {str(e)}")

@db_commands.cli.command("reset")
def reset_db():
    try:
        db.drop_all()
        db.create_all()
        seed_tables()
        print("Database reset and seeded successfully")
    except SQLAlchemyError as e:
        print(f"An error occurred while resetting the database: {str(e)}")