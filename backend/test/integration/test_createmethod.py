import unittest
from unittest.mock import patch, MagicMock
import pytest
from pymongo import MongoClient
from pymongo.errors import WriteError

from src.util.dao import DAO

@pytest.fixture(scope='session') #session, db only for this test session
def mongo_database():
    # Set up the MongoDB test database connection
    client = MongoClient('mongodb://localhost:27017')
    database = client['test_database']

    yield database

    # Clean up the test database after the test session
    client.drop_database('test_database')

# todo if time: make a better not hard-coded validation and test

@pytest.fixture
def sut(mongo_database):
    # Patch the getValidator function in the src.util.dao module
    with patch('src.util.dao.getValidator') as validator_mock:
        # Set the return value of the patched function to your desired test validator schema
        validator_mock.return_value = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["firstName", "lastName", "email"],
                "properties": {
                    "firstName": {
                        "bsonType": "string",
                        "description": "the first name of a user must be determined"
                    }, 
                    "lastName": {
                        "bsonType": "string",
                        "description": "the last name of a user must be determined"
                    },
                    "email": {
                        "bsonType": "string",
                        "description": "the email address of a user must be determined",
                        "unique": True
                    }
                }
            }
        }

        # Create an instance of the DAO with the test collection name
        dao = DAO('test_collection')

        return dao

# complete data, return object
@pytest.mark.integration
def test_create_valid_data(sut):
    # Arrange
    data = {'firstName': 'Adam', 'lastName': 'Adamsson', 'email': 'adam@adamsson.se'}

    # Act
    result = sut.create(data)

    # Assert
    assert result is not None
    assert result['firstName'] == 'Adam'
    assert result['lastName'] == 'Adamsson'
    assert result['email'] == 'adam@adamsson.se'
    assert result ['_id'] is not None

# not complete data, raise write error
@pytest.mark.integration
def test_create_missing_property(sut):
    # Arrange
    data = {'firstName': 'Adam', 'email': 'adam@adamsson.se'}

    # Act
    with pytest.raises(WriteError):
        sut.create(data)

# complete data, wrong type, raise write error
@pytest.mark.integration
def test_create_invalid_data_type(sut):
    # Arrange
    data = {'firstName': 'Adam', 'city': 'Ankeborg', 'email': 'adam@adamsson.se'}

    # Act
    with pytest.raises(WriteError):
        sut.create(data)

# complete data, not unik, raise write error
@pytest.mark.integration
def test_create_duplicate_unique_property(sut):
    data = {'firstName': 'Adam', 'lastName': 'Adamsson', 'email': 'adam@adamsson.se'}

    # Insert a document with the same email into the collection
    result = sut.create(data)

    # Act
    with pytest.raises(WriteError):
        sut.create(data)

# no data raise write error
@pytest.mark.integration
def test_create_empty_data(sut):
    data = {}

    # Act
    with pytest.raises(WriteError):
        sut.create(data)


