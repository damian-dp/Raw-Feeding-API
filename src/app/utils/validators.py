import re
from datetime import datetime, date
import bleach
from email_validator import validate_email as validate_email_format, EmailNotValidError

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

def validate_date_of_birth(date_input):
    try:
        if isinstance(date_input, str):
            dob = datetime.strptime(date_input, '%Y-%m-%d').date()
        elif isinstance(date_input, datetime):
            dob = date_input.date()
        else:
            dob = date_input
        
        today = date.today()
        if dob > today:
            return False, "Date of birth cannot be in the future"
        return True, None
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD"

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

def validate_dog_name_or_breed(value):
    return bool(value) and len(value) <= 50

def validate_profile_image_url(url):
    return isinstance(url, str) and len(url) <= 255

def validate_recipe_instructions(instructions):
    return isinstance(instructions, str) and len(instructions) > 0

def validate_recipe_description(description):
    return isinstance(description, str)

def validate_id_list(id_list):
    return isinstance(id_list, list) and all(isinstance(id, int) for id in id_list)

def validate_unit(unit):
    # Unit should be a non-empty string with a maximum length of 20 characters
    return isinstance(unit, str) and 0 < len(unit) <= 20

def validate_is_public(is_public):
    return isinstance(is_public, bool)

def validate_ingredient_id(ingredient_id):
    return isinstance(ingredient_id, int) and ingredient_id > 0

def validate_user_id(user_id):
    return isinstance(user_id, int) and user_id > 0

def sanitize_string(input_string):
    return bleach.clean(input_string, strip=True)

def validate_and_sanitize_email(email):
    try:
        valid = validate_email_format(email)
        return valid.email, None
    except EmailNotValidError as e:
        return None, str(e)

def validate_date_format(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None