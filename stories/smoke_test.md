# Story: TestSquad Automation Smoke Test

**Persona**: QA Engineer
**Goal**: Verify that the baseline automation repository can communicate with the TestSquad API and UI.

## Acceptance Criteria
1. **API Readiness**: A health check request to the TestSquad backend returns 200 OK.
2. **UI Readiness**: The Playwright runner can load the TestSquad login page.
3. **Structure**: The `testsquad-automation` directory contains the granular structure defined in the planning phase.

## Gherkin Scenario
```gherkin
Feature: Automation Repo Smoke Test

  Scenario: Repository Skeleton and Connectivity
    Given the "testsquad-automation" repository is initialized
    When I run the API health check test
    Then the TestSquad server should respond with 200 OK
    And the UI smoke test should load the dashboard page
```
