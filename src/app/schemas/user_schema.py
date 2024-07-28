from ..models.user import User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)
        ordered = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)