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

    recipes = db.relationship('Recipe', secondary='dog_recipe', back_populates='dogs')

    def __init__(self, **kwargs):
        super(Dog, self).__init__(**kwargs)
        self.calculate_age()

    def calculate_age(self):
        today = datetime.now().date()
        self.age = relativedelta(today, self.date_of_birth).years

db.event.listen(Dog, 'before_insert', lambda mapper, connection, target: target.calculate_age())
db.event.listen(Dog, 'before_update', lambda mapper, connection, target: target.calculate_age())