import pytest
from fastapi.testclient import TestClient

# Assuming the FastAPI app instance is in src.server.app
# The 'app' object is the instance of the FastAPI application.
from src.server.app import app

client = TestClient(app)


def test_validate_email_endpoint_valid_email():
    """
    Tests the /validate-email/ endpoint with a valid email, expecting a 200 OK response.
    """
    # Arrange
    request_data = {"email": "valid.email@example.com"}

    # Act
    response = client.post("/validate-email/", json=request_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Email is valid"}


def test_validate_email_endpoint_invalid_email_format():
    """
    Tests the /validate-email/ endpoint with an invalid email format, 
    expecting a 422 Unprocessable Entity response.
    """
    # Arrange
    request_data = {"email": "invalid-email-format"}

    # Act
    response = client.post("/validate-email/", json=request_data)

    # Assert
    assert response.status_code == 422
    response_data = response.json()
    assert "detail" in response_data
    assert isinstance(response_data["detail"], list)
    assert len(response_data["detail"]) == 1
    assert response_data["detail"][0]["loc"] == ["body", "email"]
    assert "valid email address" in response_data["detail"][0]["msg"]


def test_validate_email_endpoint_missing_email_field():
    """
    Tests the /validate-email/ endpoint with a missing email field, expecting a 422 response.
    """
    # Arrange
    request_data = {"other_field": "some_value"}  # 'email' field is missing

    # Act
    response = client.post("/validate-email/", json=request_data)

    # Assert
    assert response.status_code == 422
    response_data = response.json()
    assert "detail" in response_data
    assert isinstance(response_data["detail"], list)
    assert len(response_data["detail"]) == 1
    assert response_data["detail"][0]["loc"] == ["body", "email"]
    assert "required" in response_data["detail"][0]["msg"].lower()


def test_validate_email_endpoint_with_extra_fields():
    """
    Tests that the endpoint successfully validates the email even if extra fields are present in the payload.
    """
    # Arrange
    request_data = {"email": "valid.email@example.com", "extra_field": "some_value"}

    # Act
    response = client.post("/validate-email/", json=request_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Email is valid"}
