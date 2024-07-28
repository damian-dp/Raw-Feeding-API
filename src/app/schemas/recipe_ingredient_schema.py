from ..models.recipe_ingredient import RecipeIngredient
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class RecipeIngredientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RecipeIngredient
        load_instance = True
        include_fk = True
        ordered = True

    recipe_id = fields.Integer(allow_none=True)
    ingredient_name = fields.String(attribute='ingredient.name')

recipe_ingredient_schema = RecipeIngredientSchema()
recipe_ingredients_schema = RecipeIngredientSchema(many=True)