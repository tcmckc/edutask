import pytest

# mock

from src.controllers.usercontroller import UserController

def test_valid_existing_email():
    email = "test@example.com"  # Valid existing email
    user = UserController(email)
    assert user is not None

def test_valid_existing_email_multiple_users():
    email = "test@example.com"  # Valid existing email with multiple users
    with pytest.raises(Exception) as e:
        user = UserController(email)
    assert str(email) in str(e.value)

def test_valid_non_existing_email():
    email = "nonexistent@example.com"  # Valid email but does not exist in the database
    user = UserController(email)
    assert user is None

def test_invalid_email_format():
    email = "invalid_email"  # Invalid email format
    with pytest.raises(ValueError):
        UserController(email)

def test_database_operation_failure():
    email = "test@example.com"  # Valid existing email
    # Simulate a database operation failure and assert the Exception
    with pytest.raises(Exception):
        UserController(email)