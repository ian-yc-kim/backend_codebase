import pytest
from src.backend_codebase.services import signup, hash_password


def test_hash_password():
    password = "securepassword123"
    hashed = hash_password(password)
    assert hashed != password
    assert isinstance(hashed, str)


def test_signup():
    username = "testuser"
    password = "securepassword123"
    result = signup(username, password)
    assert result['username'] == username
    assert result['hashed_password'] != password
    assert isinstance(result['hashed_password'], str)
