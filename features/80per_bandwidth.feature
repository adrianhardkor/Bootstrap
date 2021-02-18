Feature: Test Ping Functionality
  @demo @XT-229
  Scenario: 60MB/10MB
    Given TIER
    When I try to run "Test 60MB/10MB speed tier"
    Then I expect "80" percent provisioned bandwidth
  Scenario: 60MB/10MB
    Given TIER
    When I try to run "Test 240MB/15MB speed tier"
    Then I expect "80" percent provisioned bandwidth
  Scenario: 60MB/10MB
    Given TIER
    When I try to run "Test 600MB/40MB speed tier"
    Then I expect "80" percent provisioned bandwidth
  Scenario: 60MB/10MB
    Given TIER
    When I try to run "Test 1G/50MB speed tier"
    Then I expect "80" percent provisioned bandwidth



UBB
 Given: UBB topology + 2 modems @ vlan, traffic profile 1024B at 25MBps per modem -- is Given already in CI/CD GIT REPO?
 When: Traffic runs
 Then: 
