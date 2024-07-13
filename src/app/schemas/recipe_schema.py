from ..extensions import ma
from ..models.recipe import Recipe

class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        load_instance = True
        include_fk = True

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)