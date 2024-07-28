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
    # Relationship: One-to-Many with RecipeIngredient model
    # This relationship allows easy access to all ingredients in this recipe
    # The 'cascade' parameter ensures that when a recipe is deleted, its ingredients are also deleted
    ingredients = db.relationship('RecipeIngredient', back_populates='recipe', cascade="all, delete-orphan")

    # Relationship: Many-to-Many with Dog model
    # This relationship allows easy access to all dogs associated with this recipe
    # The 'secondary' parameter specifies the association table for the many-to-many relationship
    dogs = db.relationship('Dog', secondary='dog_recipe', back_populates='recipes')

    @property
    def total_calories(self):
        """
        Calculate the total calories for the recipe.
        
        This property sums the calories of each ingredient, multiplied by its quantity.
        It iterates through all RecipeIngredient objects associated with this recipe.
        
        Returns:
            float: The total calories of the recipe.
        """
        return sum(ri.ingredient.calories * ri.quantity for ri in self.ingredients)

    @property
    def total_protein(self):
        """
        Calculate the total protein content for the recipe.
        
        This property sums the protein content of each ingredient, multiplied by its quantity.
        It iterates through all RecipeIngredient objects associated with this recipe.
        
        Returns:
            float: The total protein content of the recipe.
        """
        return sum(ri.ingredient.protein * ri.quantity for ri in self.ingredients)

    @property
    def total_fat(self):
        """
        Calculate the total fat content for the recipe.
        
        This property sums the fat content of each ingredient, multiplied by its quantity.
        It iterates through all RecipeIngredient objects associated with this recipe.
        
        Returns:
            float: The total fat content of the recipe.
        """
        return sum(ri.ingredient.fat * ri.quantity for ri in self.ingredients)

    @property
    def dog_ids(self):
        """
        Get the IDs of all dogs associated with this recipe.
        
        This property returns a list of dog IDs for easy serialization.
        It accesses the 'dogs' relationship and extracts the ID of each associated Dog object.
        
        Returns:
            list: A list of dog IDs associated with the recipe.
        """
        return [dog.id for dog in self.dogs]