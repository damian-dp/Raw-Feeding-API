from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db
from sqlalchemy.exc import IntegrityError

class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        try:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                access_token = create_access_token(identity=user.id)
                return {'access_token': access_token}, 200
            return {'error': 'Invalid username or password'}, 401
        except Exception as e:
            return {'error': 'An unexpected error occurred during authentication'}, 500

    @staticmethod
    def register_user(username, email, password):
        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return new_user, 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username or email already exists'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': 'An unexpected error occurred during registration'}, 500