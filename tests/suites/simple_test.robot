*** Settings ***
Documentation     Simple test to verify basic Robot Framework functionality
Library           SeleniumLibrary

*** Test Cases ***
Test Basic Browser Functionality
    [Documentation]    Simple test to verify Chrome browser works
    Open Browser    https://www.google.com    Chrome
    Title Should Be    Google
    Close Browser
