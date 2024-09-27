import pytest
from backend_codebase.validation import validate_username, validate_email_address, validate_password

# Test cases for validate_username
def test_validate_username_valid():
    assert validate_username('valid_user') is True
    assert validate_username('user123') is True
    assert validate_username('user_name_123') is True

def test_validate_username_invalid():
    assert validate_username('us') is False  # Too short
    assert validate_username('u' * 31) is False  # Too long
    assert validate_username('invalid user') is False  # Space not allowed
    assert validate_username('invalid-user') is False  # Hyphen not allowed

# Test cases for validate_email_address
def test_validate_email_address_valid():
    assert validate_email_address('test@example.com') is True
    assert validate_email_address('user.name+tag+sorting@example.com') is True

def test_validate_email_address_invalid():
    assert validate_email_address('plainaddress') is False
    assert validate_email_address('@@missingusername.com') is False
    assert validate_email_address('username@.com') is False

# Test cases for validate_password
def test_validate_password_valid():
    assert validate_password('Password123') is True
    assert validate_password('Another1') is True

def test_validate_password_invalid():
    assert validate_password('short1') is False  # Too short
    assert validate_password('nouppercase1') is False  # No uppercase letter
    assert validate_password('NOLOWERCASE1') is False  # No lowercase letter
    assert validate_password('NoDigits') is False  # No digit
