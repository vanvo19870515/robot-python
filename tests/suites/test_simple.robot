*** Settings ***
Documentation     Simple test to verify environment setup
Library           SeleniumLibrary

*** Test Cases ***
Test Basic Setup
    [Documentation]    Simple test to verify Robot Framework is working
    Log    Environment setup is working correctly
    Should Be True    True    Basic test passed
