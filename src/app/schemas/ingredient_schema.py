from ..models.ingredient import Ingredient
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class IngredientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ingredient
        load_instance = True
        include_fk = True
        ordered = True

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)