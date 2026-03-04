from src.agent.test_generator import generate_tests_with_reasoning


def test_generate_tests_with_reasoning_is_plausible():
    """
    Tests that generate_tests_with_reasoning produces a plausible test code
    and reasoning string for a simple function.
    """
    # Arrange: Define a simple Python function as a string.
    source_code_to_test = "def add(a, b):\n    return a + b"

    # Act: Call the function with the input.
    generated_test, reasoning = generate_tests_with_reasoning(source_code_to_test)

    # Assert:
    # 1. The output should be a tuple of two non-empty strings.
    assert isinstance(generated_test, str)
    assert generated_test
    assert isinstance(reasoning, str)
    assert reasoning

    # 2. The generated test should contain plausible test code constructs.
    assert "def test_add" in generated_test
    assert "assert add(" in generated_test

    # 3. The reasoning should contain some explanatory text about the function.
    assert "add" in reasoning
