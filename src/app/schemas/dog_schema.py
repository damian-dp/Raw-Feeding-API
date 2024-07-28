from ..extensions import ma
from ..models.dog import Dog
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class DogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Dog
        load_instance = True
        include_fk = True
        ordered = True

    id = ma.Integer(dump_only=True)
    name = ma.String(required=True)
    breed = ma.String(required=True)
    date_of_birth = ma.Date(required=True)
    weight = ma.Float(required=True)
    profile_image = ma.String()
    user_id = ma.Integer(allow_none=True)
    age = ma.Integer(dump_only=True)
    recipes = ma.List(ma.Integer(), dump_only=True)

dog_schema = DogSchema()
dogs_schema = DogSchema(many=True)