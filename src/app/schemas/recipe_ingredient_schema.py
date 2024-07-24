from ..extensions import ma
from ..models.recipe_ingredient import RecipeIngredient
from marshmallow import fields

class RecipeIngredientSchema(ma.SQLAlchemyAutoSchema):
    ingredient_name = fields.String(attribute='ingredient.name')

    class Meta:
        model = RecipeIngredient
        load_instance = True
        include_fk = True

recipe_ingredient_schema = RecipeIngredientSchema()
recipe_ingredients_schema = RecipeIngredientSchema(many=True)