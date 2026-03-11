import pytest
from src.agent.config import parse_frontmatter

def test_parse_frontmatter_with_valid_yaml():
    """
    Tests parsing a string with valid YAML frontmatter and content.
    """
    # Arrange
    content = """---
title: "Hello World"
author: "John Doe"
---
This is the content.
"""
    expected_frontmatter = {"title": "Hello World", "author": "John Doe"}
    expected_content = "This is the content.\n"

    # Act
    frontmatter, remaining_content = parse_frontmatter(content)

    # Assert
    assert frontmatter == expected_frontmatter
    assert remaining_content == expected_content

@pytest.mark.parametrize(
    "content_input",
    [
        "Just content.",
        # Not at the start of the string
        "\n---\ntitle: test\n---\nContent",
        # Looks like frontmatter but isn't at the start
        "Some text\n---\ntitle: test\n---\nContent",
    ],
    ids=[
        "no_delimiters",
        "delimiter_not_at_start_newline",
        "delimiter_not_at_start_text",
    ]
)
def test_parse_frontmatter_without_frontmatter(content_input):
    """
    Tests parsing strings that do not contain valid frontmatter at the beginning.
    The function should treat the entire string as content.
    """
    # Arrange
    expected_frontmatter = {}

    # Act
    frontmatter, remaining_content = parse_frontmatter(content_input)

    # Assert
    assert frontmatter == expected_frontmatter
    assert remaining_content == content_input

def test_parse_frontmatter_empty_string():
    """
    Tests parsing an empty string.
    """
    # Arrange
    content = ""
    expected_frontmatter = {}
    expected_content = ""

    # Act
    frontmatter, remaining_content = parse_frontmatter(content)

    # Assert
    assert frontmatter == expected_frontmatter
    assert remaining_content == expected_content

@pytest.mark.parametrize(
    "content_input, expected_content",
    [
        ("""---
title: "Only Frontmatter"
---""", ""),
        ("""---
title: "Only Frontmatter"
---\n""", "\n"),
    ],
    ids=["no_trailing_newline", "with_trailing_newline"]
)
def test_parse_frontmatter_only_frontmatter(content_input, expected_content):
    """
    Tests parsing a string that only contains frontmatter.
    """
    # Arrange
    expected_frontmatter = {"title": "Only Frontmatter"}

    # Act
    frontmatter, remaining_content = parse_frontmatter(content_input)

    # Assert
    assert frontmatter == expected_frontmatter
    assert remaining_content == expected_content

def test_parse_frontmatter_empty_frontmatter_block():
    """
    Tests parsing a string with an empty frontmatter block.
    """
    # Arrange
    content = """---
---
Some content here.
"""
    expected_frontmatter = {}
    expected_content = "Some content here.\n"

    # Act
    frontmatter, remaining_content = parse_frontmatter(content)

    # Assert
    assert frontmatter == expected_frontmatter
    assert remaining_content == expected_content

def test_parse_frontmatter_malformed_yaml():
    """
    Tests that malformed YAML in the frontmatter raises a ValueError.
    """
    # Arrange
    content = """---
title: "Incomplete
author: "Missing Quote
---
Content
"""
    # Act & Assert
    # Assuming the function wraps the YAML parsing error in a ValueError.
    with pytest.raises(ValueError, match="Failed to parse YAML frontmatter"):
        parse_frontmatter(content)

def test_parse_frontmatter_no_closing_delimiter():
    """
    Tests parsing a string with an opening delimiter but no closing one.
    This should be treated as not having frontmatter.
    """
    # Arrange
    content = """---
title: "No closing tag"
Some content.
"""
    expected_frontmatter = {}

    # Act
    frontmatter, remaining_content = parse_frontmatter(content)

    # Assert
    assert frontmatter == expected_frontmatter
    assert remaining_content == content

def test_parse_frontmatter_with_complex_yaml_types():
    """
    Tests parsing frontmatter with various YAML data types.
    """
    # Arrange
    content = """---
title: My Post
published: true
tags:
  - code
  - python
  - testing
metadata:
  views: 1024
  likes: 42
---
Content follows.
"""
    expected_frontmatter = {
        "title": "My Post",
        "published": True,
        "tags": ["code", "python", "testing"],
        "metadata": {"views": 1024, "likes": 42},
    }
    expected_content = "Content follows.\n"

    # Act
    frontmatter, remaining_content = parse_frontmatter(content)

    # Assert
    assert frontmatter == expected_frontmatter
    assert remaining_content == expected_content
