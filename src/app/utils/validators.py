import re
from datetime import datetime

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    # Password should be at least 8 characters long and contain at least one uppercase letter, 
    # one lowercase letter, one digit, and one special character
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password) is not None

def validate_username(username):
    # Username should be 3-20 characters long and contain only letters, numbers, and underscores
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

def validate_date_of_birth(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_weight(weight):
    try:
        weight_float = float(weight)
        return 0 < weight_float < 200  # Assuming weight is in kg and max dog weight is 200kg
    except ValueError:
        return False

def validate_ingredient_name(name):
    # Ingredient name should be 2-50 characters long and contain only letters, numbers, spaces, and hyphens
    pattern = r'^[a-zA-Z0-9 -]{2,50}$'
    return re.match(pattern, name) is not None

def validate_recipe_name(name):
    # Recipe name should be 3-100 characters long
    return 3 <= len(name) <= 100

def validate_quantity(quantity):
    try:
        quantity_float = float(quantity)
        return quantity_float > 0
    except ValueError:
        return False