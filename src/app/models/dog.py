from ..extensions import db
from datetime import datetime
from sqlalchemy import event
from dateutil.relativedelta import relativedelta

class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    breed = db.Column(db.String(64))
    date_of_birth = db.Column(db.Date)
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)  # in kg
    profile_image = db.Column(db.String(255))  # URL to image
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recipes = db.relationship('Recipe', secondary='dog_recipe', back_populates='dogs')

    def __repr__(self):
        return f'<Dog {self.name}>'

def calculate_age(target, value, oldvalue, initiator):
    if value is not None:
        today = datetime.utcnow().date()
        age = relativedelta(today, value).years
        target.age = age

event.listen(Dog.date_of_birth, 'set', calculate_age)

@event.listens_for(Dog, 'before_insert')
@event.listens_for(Dog, 'before_update')
def update_age(mapper, connection, target):
    if target.date_of_birth:
        today = datetime.utcnow().date()
        age = relativedelta(today, target.date_of_birth).years
        target.age = age