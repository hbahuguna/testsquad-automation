import pytest
from pydantic import ValidationError

# Assuming EmailValidationRequest is in src.server.app
# This test file assumes the following Pydantic model exists:
#
# from pydantic import BaseModel, EmailStr
#
# class EmailValidationRequest(BaseModel):
#     email: EmailStr

from src.server.app import EmailValidationRequest


@pytest.mark.parametrize(
    "valid_email",
    [
        "test@example.com",
        "test.name@example.co.uk",
        "test+alias@example.com",
        "test_underscore@example.com",
        "test-hyphen@example.com",
        "12345@example.com",
    ],
)
def test_email_validation_request_valid_emails(valid_email):
    """
    Tests that EmailValidationRequest successfully validates various correct email formats.
    """
    # Arrange
    request_data = {"email": valid_email}

    # Act
    instance = EmailValidationRequest(**request_data)

    # Assert
    assert instance.email == valid_email


@pytest.mark.parametrize(
    "invalid_email",
    [
        "plainaddress",
        "@missingusername.com",
        "username@.com",
        "username@domain..com",
        "username@domain.com.",
        "test@",
        "",
        " leading.space@example.com",
        "trailing.space@example.com ",
    ],
)
def test_email_validation_request_invalid_email_format(invalid_email):
    """
    Tests that EmailValidationRequest raises ValidationError for incorrectly formatted emails.
    """
    # Arrange
    request_data = {"email": invalid_email}

    # Act & Assert
    with pytest.raises(ValidationError):
        EmailValidationRequest(**request_data)


def test_email_validation_request_missing_email_field():
    """
    Tests that EmailValidationRequest raises ValidationError when the 'email' field is missing.
    """
    # Arrange
    request_data = {}

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        EmailValidationRequest(**request_data)

    # Assert on error details
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("email",)
    assert "required" in errors[0]["msg"]


@pytest.mark.parametrize(
    "non_string_value",
    [
        123,
        123.45,
        True,
        [],
        {},
        b"not a string",
    ],
)
def test_email_validation_request_non_string_email(non_string_value):
    """
    Tests that EmailValidationRequest raises ValidationError when the 'email' field is not a string.
    """
    # Arrange
    request_data = {"email": non_string_value}

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        EmailValidationRequest(**request_data)

    # Assert on error details
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("email",)
    error_msg = errors[0]["msg"].lower()
    assert "string" in error_msg or "str" in error_msg


def test_email_validation_request_none_email():
    """
    Tests that EmailValidationRequest raises ValidationError when the 'email' field is None.
    """
    # Arrange
    request_data = {"email": None}

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        EmailValidationRequest(**request_data)

    # Assert on error details
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("email",)
    error_msg = errors[0]["msg"].lower()
    # Pydantic v1: 'none is not an allowed value', Pydantic v2: 'Input should be a valid string'
    assert "none" in error_msg or "string" in error_msg
