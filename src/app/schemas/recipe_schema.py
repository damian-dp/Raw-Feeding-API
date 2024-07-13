from app import ma
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient

class RecipeIngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecipeIngredient
        include_fk = True

class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        include_fk = True
    
    ingredients = ma.Nested(RecipeIngredientSchema, many=True)

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)
