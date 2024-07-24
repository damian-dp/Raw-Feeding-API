from ..extensions import db
from datetime import datetime

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    ingredients = db.relationship('RecipeIngredient', back_populates='recipe', cascade="all, delete-orphan")
    dogs = db.relationship('Dog', secondary='dog_recipe', back_populates='recipes')

    @property
    def total_calories(self):
        return sum(ri.ingredient.calories * ri.quantity for ri in self.ingredients)

    @property
    def total_protein(self):
        return sum(ri.ingredient.protein * ri.quantity for ri in self.ingredients)

    @property
    def total_fat(self):
        return sum(ri.ingredient.fat * ri.quantity for ri in self.ingredients)

    @property
    def dog_ids(self):
        return [dog.id for dog in self.dogs]