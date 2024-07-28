from ..extensions import ma
from ..models.dog import Dog

class DogSchema(ma.SQLAlchemyAutoSchema):
    user_id = ma.Integer(allow_none=True)
    class Meta:
        model = Dog
        load_instance = True
        recipes = ma.List(ma.Integer())
        include_fk = True

dog_schema = DogSchema()
dogs_schema = DogSchema(many=True)