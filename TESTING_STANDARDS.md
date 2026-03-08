# Testing Standards

## 1. General Principles

- **File Naming**: Python test files must be prefixed with `test_` (e.g., `test_core.py`). E2E test files must end with `.spec.ts` (e.g., `test_login.spec.ts`).
- **Function Naming**: Test functions must be prefixed with `test_`.
- **Structure**: Tests follow an Arrange-Act-Assert pattern. Setup logic is often encapsulated in fixtures or commented sections.
- **Documentation**: Each test function should have a concise docstring describing the test's purpose, often starting with `Scenario:`.

## 2. Backend Testing (Python / Pytest)

- **Framework & Runner**: All Python tests use `pytest`.
- **Assertions**: Use the standard Python `assert` statement for all validations.
  - `assert result["status"] == "pass"`
  - `assert "Error Message" in result["error"]`
- **Mocking Strategy**: Use the standard `unittest.mock` library.
  - **Method**: Apply mocks as function decorators: `@patch("src.module.function_to_mock")`.
  - **Configuration**: Mocks are passed as arguments to the test function. Configure their behavior directly: `mock_run.return_value = Mock(stdout="...")`.
- **Fixtures & Setup**:
  - **Decorator**: Use `@pytest.fixture` to define setup/teardown logic.
  - **Pattern**: Fixtures frequently use `tempfile.TemporaryDirectory` and `pathlib.Path` to create isolated filesystem environments.
  - **Lifecycle**: Use `yield` within a `with` block to provide the resource to the test and ensure cleanup.

## 3. Frontend Testing (TypeScript / Playwright)

- **Framework**: E2E tests are written using Playwright.
- **Test Definition**: Tests are defined using the `test()` function from `@playwright/test`.
  - `test('login flow', async ({ page }) => { ... });`

## 4. Test Discovery & Typing

The test system automatically categorizes tests based on file extension:
- `*.py` files are tagged as `unit` tests.
- `*.spec.ts` files are tagged as `e2e` tests.