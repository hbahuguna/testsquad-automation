Feature: PR Analysis Validation and Ingestion
  As a user triggering the Test Execution workflow,
  I want the Agent to reliably read the workspace and create a PR,
  So that I don't get "insufficient data" errors caused by the Agent arbitrarily grepping the PR ID.

  Scenario: Agent successfully creates PR for generated tests without generic grep errors
    Given a PR has been successfully analysed and tests generated in the workspace
    When the user clicks "Open Pull Request" for the PR
    Then the Agent retrieves the workspace paths and the PR diff using MCP tools
    And the Agent does not abort with "insufficient data to proceed"
    And a new Pull Request is successfully opened with the generated tests
