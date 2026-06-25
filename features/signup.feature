Feature: Signup Functionality

  Background:
    Given the user accepts the notifications pop-up

  @sign_up_flow
  Scenario: New user onboarding E2E flow
    Given the user enters valid email id and otp
    And clicks the otp continue button
    Then the user should be asked to enter the phone number
    When user enters the phone number
    And click on the phone number continue button
    And user enters the OTP and clicks on the continue button
    Then user asked to select the language
    When user selects the language and clicks on continue button


    Then user should be asked to connect the Luna Ring
    When user click on search now button 
    Then user should be asked to allow to access location permission
    And user grands the location access
    Then near by luna rings shoudld be detected and displayed
    When user selects the luna ring 
    Then pairing should start 
    And after pairing is copleted user should be asked to enter user name
    When user enters the name and clicks on continue button
    Then user should be asked to enter date of birth
    When user enters the date of birth and clicks on continue button
    Then user should be asked to select the gender
    When user selects the gender and clicks on continue button  
    Then user should be asked to enter users height
    When user select the height and clicks on continue button
    Then user should be asked to enter users weight
    When user enters the weight and clicks on continue button 
    Then user should be asked to select the the intent of use
    When user selects the intent of use and clicks on continue button  
    Then user lands on all done page
    When user click on let's go button
    Then user lands on home page screen


   

    
