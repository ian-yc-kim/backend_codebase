import re
from email_validator import validate_email, EmailNotValidError


def validate_username(username: str) -> bool:
    """
    Validate the username to ensure it meets the length and character requirements.
    - Must be between 3 and 30 characters long.
    - Can only contain alphanumeric characters and underscores.
    """
    if not (3 <= len(username) <= 30):
        return False
    if not re.match(r'^\w+$', username):
        return False
    return True


def validate_email_address(email: str) -> bool:
    """
    Validate the email format using the email-validator package.
    """
    try:
        # Disable DNS and deliverability checks
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


def validate_password(password: str) -> bool:
    """
    Validate the password to ensure it meets the length and character requirements.
    - Must be at least 8 characters long.
    - Must contain at least one uppercase letter, one lowercase letter, and one digit.
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True
