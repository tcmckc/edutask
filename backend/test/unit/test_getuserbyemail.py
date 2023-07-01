import pytest
import unittest.mock as mock


from src.controllers.usercontroller import UserController

def test_valid_existing_email():
    # Create a mock DAO object
    mock_dao = mock.MagicMock()
    mock_dao.find.return_value = [{'name': 'John', 'email': 'test@example.com'}]

    # Create an instance of UserController with the mock DAO
    user_controller = UserController(dao=mock_dao)

    # Call the method being tested
    user = user_controller.get_user_by_email('test@example.com')

    # Assertions
    assert user is not None
    assert user['name'] == 'John'

def test_valid_existing_email_multiple_users():
    # Create a mock DAO object
    mock_dao = mock.MagicMock()
    mock_dao.find.return_value = [{'name': 'John', 'email': 'test@example.com'}, {'name': 'Jane', 'email': 'test@example.com'}]

    # Create an instance of UserController with the mock DAO
    user_controller = UserController(dao=mock_dao)

    # Call the method being tested and assert the exception message
    with pytest.raises(Exception) as e:
        user_controller.get_user_by_email('test@example.com')

    assert 'Error: more than one user found with mail test@example.com' in str(e.value)


def test_valid_non_existing_email():
    # Create a mock DAO object
    mock_dao = mock.MagicMock()
    mock_dao.find.return_value = []  # Simulating an empty result for the email search

    # Create an instance of UserController with the mock DAO
    user_controller = UserController(dao=mock_dao)

    # Call the method being tested
    user = user_controller.get_user_by_email('nonexistent@example.com')

    # Assertions
    assert user is None

def test_invalid_email_format():
    email = "invalid_email"  # Invalid email format

    # Create an instance of UserController
    user_controller = UserController(dao=None)  # Pass a mock or None for the DAO argument

    # Call the method being tested and assert the raised ValueError
    with pytest.raises(ValueError):
        user_controller.get_user_by_email(email)

def test_database_operation_failure():
    email = "test@example.com"  # Valid existing email

    # Create a mock DAO object
    mock_dao = magic.MagicMock()
    mock_dao.find.side_effect = Exception("Simulated database operation failure")

    # Create an instance of UserController with the mock DAO
    user_controller = UserController(dao=mock_dao)

    # Call the method being tested and assert the raised Exception
    with pytest.raises(Exception) as e:
        user_controller.get_user_by_email(email)

    assert str(e.value) == "Simulated database operation failure"