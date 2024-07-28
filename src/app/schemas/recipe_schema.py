from ..models.recipe import Recipe
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .recipe_ingredient_schema import RecipeIngredientSchema

class RecipeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        load_instance = True
        include_fk = True
        include_relationships = True
        exclude = ('dogs', 'user')
        ordered = True

    dog_ids = fields.List(fields.Integer())
    ingredients = fields.Nested(RecipeIngredientSchema, many=True)
    user_id = fields.Integer(allow_none=True)

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)