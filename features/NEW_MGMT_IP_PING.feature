Feature: Test Ping Functionality
  @demo @XT-229
  Scenario: PING_EXPECTED_TRUE
    Given Bootstrap Ran
    When I try to ping NewMgmtIP from Jenkinsfile-paramter-input cidr
    Then I expect response "True"
