from app import ma
from app.models.ingredient import Ingredient

class IngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingredient
        load_instance = True

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)