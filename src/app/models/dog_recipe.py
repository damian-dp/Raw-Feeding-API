from ..extensions import db

dog_recipe = db.Table('dog_recipe',
    db.Column('dog_id', db.Integer, db.ForeignKey('dog.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)
