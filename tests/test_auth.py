import pytest
from app.backend import managers


@pytest.fixture
def mock_auth_service(mocker):
    return mocker.Mock()


@pytest.fixture
def auth_manager(mock_auth_service):
    return managers.AuthManager(auth_service=mock_auth_service)


def test_validate_creds_valid(auth_manager):
    creds = {
        "user": "john",
        "email": "john@example.com",
        "pass": "123456",
        "confirm_pass": "123456"
    }
    assert auth_manager.validate_creds(creds) is True


def test_validate_creds_invalid_passwords(auth_manager):
    creds = {
        "user": "john",
        "email": "john@example.com",
        "pass": "123456",
        "confirm_pass": "654321"  # Passwords do not match
    }
    assert auth_manager.validate_creds(creds) is False


def test_validate_creds_invalid_email(auth_manager):
    creds = {
        "user": "john",
        "email": "johnexample.com",  # Invalid email format
        "pass": "123456",
        "confirm_pass": "123456"
    }
    assert auth_manager.validate_creds(creds) is False
