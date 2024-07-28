from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db
from sqlalchemy.exc import IntegrityError

class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        try:
            # Query the database to find a user with the given username
            # This uses the filter_by method to search for an exact match
            # and the first method to return only one result or None
            user = User.query.filter_by(username=username).first()

            # Check if the user exists and the password is correct
            # The check_password method is a custom method on the User model
            # that compares the given password with the stored hash
            if user and user.check_password(password):
                # Create a JWT access token for the authenticated user
                # The user's ID is used as the identity in the token
                access_token = create_access_token(identity=user.id)
                return {'access_token': access_token}, 200
            return {'error': 'Invalid username or password'}, 401
        except Exception as e:
            return {'error': 'An unexpected error occurred during authentication'}, 500

    @staticmethod
    def register_user(username, email, password):
        try:
            # Create a new User instance with the provided username and email
            # The password is not set directly here for security reasons
            new_user = User(username=username, email=email)

            # Set the password using a custom method on the User model
            # This method typically hashes the password before storing it
            new_user.set_password(password)

            # Add the new user to the database session
            # This stages the new user for insertion into the database
            db.session.add(new_user)

            # Commit the transaction to persist the new user in the database
            # If this succeeds, the user is now stored in the database
            db.session.commit()

            return new_user, 201
        except IntegrityError:
            # Roll back the session if there's an integrity error
            # This typically occurs if the username or email already exists
            db.session.rollback()
            return {'error': 'Username or email already exists'}, 409
        except Exception as e:
            # Roll back the session for any other unexpected errors
            db.session.rollback()
            return {'error': 'An unexpected error occurred during registration'}, 500