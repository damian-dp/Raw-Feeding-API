from ..extensions import db

# Association table for the many-to-many relationship between Dog and Recipe
# This table doesn't have its own model class as it's a simple junction table
dog_recipe = db.Table('dog_recipe',
    # Foreign key referencing the Dog model's id
    db.Column('dog_id', db.Integer, db.ForeignKey('dog.id'), primary_key=True),
    # Foreign key referencing the Recipe model's id
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)