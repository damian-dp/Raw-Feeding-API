from ..extensions import db
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    profile_image = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer)

    # Relationship: Many-to-Many with Recipe model
    # This relationship allows easy access to all recipes associated with this dog
    # The 'secondary' parameter specifies the association table for the many-to-many relationship
    recipes = db.relationship('Recipe', secondary='dog_recipe', back_populates='dogs')

    def __init__(self, **kwargs):
        """
        Initialize a new Dog instance.
        
        This method calls the parent class initializer and then calculates the dog's age.
        """
        super(Dog, self).__init__(**kwargs)
        self.calculate_age()

    def calculate_age(self):
        """
        Calculate and set the dog's age based on its date of birth.
        
        This method computes the difference between the current date and the dog's
        date of birth, setting the 'age' attribute to the number of years.
        """
        today = datetime.now().date()
        self.age = relativedelta(today, self.date_of_birth).years

# Event listeners to automatically update the dog's age before inserting or updating
db.event.listen(Dog, 'before_insert', lambda mapper, connection, target: target.calculate_age())
db.event.listen(Dog, 'before_update', lambda mapper, connection, target: target.calculate_age())