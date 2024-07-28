from ..extensions import db

class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)

    # Relationship: Many-to-One with Recipe model
    # This relationship allows easy access to the recipe this ingredient belongs to
    recipe = db.relationship('Recipe', back_populates='ingredients')

    # Relationship: Many-to-One with Ingredient model
    # This relationship allows easy access to the ingredient details
    ingredient = db.relationship('Ingredient', back_populates='recipe_ingredients')

    def __repr__(self):
        return f'<RecipeIngredient {self.recipe_id}:{self.ingredient_id}>'