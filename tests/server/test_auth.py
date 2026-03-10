import pytest
from src.server.auth import is_valid_email


@pytest.mark.parametrize("email, expected", [
    # === Valid Emails ===
    ("test@example.com", True),
    ("test.name@example.com", True),
    ("test+alias@example.com", True),
    ("test_name@example.com", True),
    ("test-name@example.com", True),
    ("123test@example.com", True),
    ("test123@example.com", True),
    ("test@sub.domain.com", True),
    ("test@example.co.uk", True),
    ("test@example.name", True),
    ("test@example-domain.com", True),
    ("TEST@EXAMPLE.COM", True),
    ("t@g.cn", True),
    ("email@domain.international", True),

    # === Invalid Emails ===
    # Structure
    ("plainaddress", False),
    ("@missing-local-part.com", False),
    ("test.example.com@", False),
    ("test@@example.com", False),
    ("", False),

    # Characters
    ("test @domain.com", False),
    ("test@ domain.com", False),
    ("test'test@domain.com", False),
    ("test@dom_ain.com", False),
    ("test@test.com\n", False),
    (" test@test.com", False),
    ("test@test.com ", False),

    # Local part
    (".test@example.com", False),
    ("test.@example.com", False),
    ("test..test@example.com", False),

    # Domain part
    ("test@.com", False),
    ("test@domain.", False),
    ("test@domain.c", False),
    ("test@domain..com", False),
    ("test@domain", False),
    ("test@domain-.com", False),
    ("test@-domain.com", False),
    ("test@domain.com-", False),
    ("test@123.123.123.123", False),

    # === Invalid Types ===
    (None, False),
    (123, False),
    (123.45, False),
    (True, False),
    ([], False),
    ({}, False),
    ((), False),
])
def test_is_valid_email(email, expected):
    """
    Test the is_valid_email function with a variety of valid, invalid,
    and edge case inputs.
    """
    assert is_valid_email(email) is expected
