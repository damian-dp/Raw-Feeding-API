from ..extensions import db
import bcrypt

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    # Relationship: One-to-Many with Dog model
    # This relationship allows easy access to all dogs owned by this user
    # The 'lazy' parameter set to 'dynamic' returns a query object instead of loading all dogs at once
    dogs = db.relationship('Dog', backref='owner', lazy='dynamic')

    # Relationship: One-to-Many with Recipe model
    # This relationship allows easy access to all recipes created by this user
    # The 'lazy' parameter set to 'dynamic' returns a query object instead of loading all recipes at once
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')

    def set_password(self, password):
        """
        Hash and set the user's password.
        
        This method uses bcrypt to securely hash the password before storing it.
        The hashed password is stored as a UTF-8 encoded string.
        
        Args:
            password (str): The plain text password to be hashed and stored.
        """
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """
        Verify a password against the stored hash.
        
        This method uses bcrypt to check if the provided password matches the stored hash.
        
        Args:
            password (str): The plain text password to be verified.
        
        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'