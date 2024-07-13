from ..extensions import db

class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)

    # Relationships
    recipe = db.relationship('Recipe', back_populates='ingredients', cascade="all, delete-orphan")
    ingredient = db.relationship('Ingredient', back_populates='recipes', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<RecipeIngredient {self.recipe_id}:{self.ingredient_id}>'
