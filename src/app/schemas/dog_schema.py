from ..extensions import ma
from ..models.dog import Dog

class DogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Dog
        load_instance = True
        include_fk = True

dog_schema = DogSchema()
dogs_schema = DogSchema(many=True)
