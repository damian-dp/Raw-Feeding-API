from ..extensions import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    category = db.Column(db.String(64))
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbohydrates = db.Column(db.Float)
    fiber = db.Column(db.Float)
    vitamins = db.Column(db.JSON)
    minerals = db.Column(db.JSON)

    # Relationships
    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='ingredient', cascade="all, delete-orphan")