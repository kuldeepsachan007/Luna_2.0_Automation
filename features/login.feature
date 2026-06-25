Feature: Login Functionality
    As a registered user User wants to log into the application
    So that they can access their personalized dashboard and features.


  Background:
    Given the user accepts the notifications pop-up


  @login
  Scenario: Successful login with valid email and otp
    Given the user enters valid email id and otp
        |email|
        |kuldeep.sachan@nexxbase.com| 
    And clicks the otp continue button
    Then user asked to select the language
    When user selects the language and clicks on continue button
    Then user should be asked to connect the Luna Ring
    When user click on search now button 
    Then user should be asked to allow to access location permission
    And user grands the location access
    Then near by luna rings shoudld be detected and displayed
    When user selects the luna ring 
    Then pairing should start 
    And user verifies the mac address of the ring is correct
    When user clicks on the Get started button
    Then user lands on the home page screen


  Scenario: Successful login using credentials
    Given the user is on the login page
    When the user enters valid credentials
    And clicks the login button
    Then the user should be redirected to the select organization page