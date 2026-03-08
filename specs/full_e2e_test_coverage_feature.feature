Feature: Full System E2E Coverage
  As a QA Engineer configuring the TestSquad Automation repository,
  I want to write comprehensive Playwright UI and API tests for the system,
  So that every major frontend and backend regression is caught by CI/CD continuously over time.

  Scenario: User performs the full Test Execution Journey via UI
    Given the user navigates to the TestSquad dashboard
    When the user selects an ingested Pull Request
    And clicks the "Analyze and Test" button
    Then the system transitions to the "Analysis" state
    And generates tests
    When the user clicks "Open Pull Request"
    Then the Agent opens a GitHub Pull Request with the generated fixes

  Scenario: System validates backend LLM chat via API
    Given the Playwright API request context is authenticated
    When a POST request is sent to `/api/chat` with an MCP tool scenario
    Then the response streams down context reasoning accurately
    And the FSM state updates in the PostgreSQL database correctly
