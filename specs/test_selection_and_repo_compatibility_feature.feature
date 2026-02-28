Feature: Test Selection and Repository Compatibility

  As a TestSquad system
  I want to automatically classify testing types and validate repository mapping
  So that the CI pipeline does not run incorrect test suites or hallucinate against incompatible codebases.

  # Invariants
  # 1. Pipeline MUST fail fast before LLM initialization if repos are definitively mismatched.
  # 2. Existing Tests MUST be tagged as "unit" unless strictly proven to be "e2e".
  # 3. LLM MUST NOT be used for compatibility checks (token conservation).

  Scenario: Product repo matches defined target repository in automation configuration
    Given a mapped "product_repo" is "hbahuguna/testsquad"
    And the "automation_repo" is "hbahuguna/testsquad-automation"
    And "hbahuguna/testsquad-automation" contains ".testsquad/config.yaml"
    When the compatibility check is executed
    And the config file declares "target_repo: hbahuguna/testsquad"
    Then the system should smoothly transition to the FSM "PLAN" state

  Scenario: Product repo mismatches the defined target repository
    Given a mapped "product_repo" is "hbahuguna/other-project"
    And the "automation_repo" is "hbahuguna/testsquad-automation"
    And the config file declares "target_repo: hbahuguna/testsquad"
    When the compatibility check is executed
    Then the system should hard fail the pipeline
    And display an error: "Configuration Mismatch: Automation repository targets a different product."

  Scenario: Legacy automation repository without configuration file
    Given the config file ".testsquad/config.yaml" does not exist
    When the compatibility check is executed
    Then the system should issue a warning in the logs
    And the system should continue to the FSM "PLAN" state (soft fallback)

  Scenario: Test Discovery correctly tags Unit vs E2E tests
    Given the filesystem contains "test_api.py" and "ui_flow.spec.ts"
    When "AutomationRepoMCP.search_tests()" is invoked
    And "ui_flow.spec.ts" contains "import { test } from '@playwright/test'"
    And "test_api.py" contains "import pytest"
    Then the returned results should tag "ui_flow.spec.ts" with 'type': 'e2e'
    And the returned results should tag "test_api.py" with 'type': 'unit'
