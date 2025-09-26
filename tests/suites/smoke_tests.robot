*** Settings ***
Documentation    Smoke Tests for nopCommerce Demo Site
...              Basic functionality validation using Robot Framework
Suite Setup      Setup Test Environment
Suite Teardown   Teardown Test Environment
Test Setup       Setup Browser
Test Teardown    Teardown Browser
Library          SeleniumLibrary
Library          OperatingSystem
Library          Collections
Resource         ../resources/locators.robot
Resource         ../resources/test_data.robot

*** Variables ***
${BASE_URL}      https://demo.nopcommerce.com
${BROWSER}       chrome
${TIMEOUT}       10

*** Test Cases ***
TC001_Verify Home Page Loads
    [Documentation]    Verify that the nopCommerce home page loads correctly
    [Tags]    smoke    home    critical
    Go To    ${BASE_URL}
    Wait Until Page Contains    nopCommerce    ${TIMEOUT}
    Page Should Contain    Welcome to our store
    Capture Page Screenshot    home_page.png
    ${title}=    Get Title
    Should Be Equal As Strings    ${title}    nopCommerce demo store

TC002_Verify Login Functionality
    [Documentation]    Test basic login functionality
    [Tags]    smoke    login    authentication
    Go To    ${BASE_URL}/login
    Wait Until Element Is Visible    //input[@id='Email']    ${TIMEOUT}
    Input Text    //input[@id='Email']    test@example.com
    Input Text    //input[@id='Password']    password123
    Click Element    //button[contains(text(),'Log in')]
    Wait Until Element Is Visible    //a[contains(text(),'Log out')]    ${TIMEOUT}
    Element Should Be Visible    //a[contains(text(),'Log out')]

TC003_Verify Product Search
    [Documentation]    Test product search functionality
    [Tags]    smoke    search    product
    Go To    ${BASE_URL}
    Input Text    //input[@id='small-searchterms']    laptop
    Click Element    //button[contains(text(),'Search')]
    Wait Until Element Is Visible    //div[@class='product-grid']    ${TIMEOUT}
    Page Should Contain    laptop
    ${product_count}=    Get Element Count    //div[@class='product-item']
    Should Be True    ${product_count} > 0    No products found

TC004_Verify Product Details
    [Documentation]    Test navigation to product details
    [Tags]    smoke    product    navigation
    Go To    ${BASE_URL}
    Wait Until Element Is Visible    //img[@alt='nopCommerce demo store']    ${TIMEOUT}
    Click Element    //img[@alt='nopCommerce demo store']
    Wait Until Element Is Visible    //div[@class='product-grid']    ${TIMEOUT}
    Click Element    (//button[contains(text(),'Add to cart')])[1]
    Wait Until Element Is Visible    //div[@class='product-name']    ${TIMEOUT}
    ${product_name}=    Get Text    //div[@class='product-name']//h1
    Should Not Be Empty    ${product_name}
    Capture Page Screenshot    product_details.png

TC005_Verify Shopping Cart
    [Documentation]    Test shopping cart functionality
    [Tags]    smoke    cart    checkout
    Go To    ${BASE_URL}
    Click Element    (//button[contains(text(),'Add to cart')])[1]
    Wait Until Element Is Visible    //span[@class='cart-label']    ${TIMEOUT}
    Click Element    //span[@class='cart-label']
    Click Element    //button[contains(text(),'Go to cart')]
    Wait Until Element Is Visible    //div[@class='table-wrapper']    ${TIMEOUT}
    Element Should Be Visible    //input[@class='qty-input']
    ${cart_items}=    Get Element Count    //tr[@class='cart-item-row']
    Should Be True    ${cart_items} > 0    Cart is empty

TC006_Verify Registration Process
    [Documentation]    Test user registration process
    [Tags]    smoke    registration    user
    Go To    ${BASE_URL}/register
    Select Radio Button    gender    M
    Input Text    //input[@id='FirstName']    Test
    Input Text    //input[@id='LastName']    User
    Input Text    //input[@id='Email']    testuser@example.com
    Input Text    //input[@id='Password']    TestPass123
    Input Text    //input[@id='ConfirmPassword']    TestPass123
    Click Element    //button[@id='register-button']
    Wait Until Element Is Visible    //div[@class='result']    ${TIMEOUT}
    Page Should Contain    Your registration completed

TC007_Verify Contact Us Form
    [Documentation]    Test contact us form functionality
    [Tags]    smoke    contact    form
    Go To    ${BASE_URL}/contactus
    Wait Until Element Is Visible    //button[contains(text(),'Submit')]    ${TIMEOUT}
    Input Text    //input[@id='FullName']    Test User
    Input Text    //input[@id='Email']    test@example.com
    Select From List By Label    //select[@name='Enquiry']    Support
    Input Text    //textarea[@id='Enquiry']    This is a test inquiry for automation testing.
    Click Element    //button[contains(text(),'Submit')]
    Wait Until Element Is Visible    //div[@class='result']    ${TIMEOUT}
    Page Should Contain    Your enquiry has been successfully sent

TC008_Verify Responsive Design
    [Documentation]    Test responsive design on mobile viewport
    [Tags]    smoke    responsive    mobile
    Go To    ${BASE_URL}
    Set Window Size    375    667    # iPhone SE size
    Wait Until Element Is Visible    //div[@class='header']    ${TIMEOUT}
    Element Should Be Visible    //div[@class='header']
    Set Window Size    1920    1080    # Back to desktop
    Element Should Be Visible    //div[@class='header']

TC009_Verify Page Navigation
    [Documentation]    Test basic page navigation
    [Tags]    smoke    navigation    basic
    Go To    ${BASE_URL}/register
    Wait Until Page Contains    Register    ${TIMEOUT}
    Page Should Contain    Register
    Go To    ${BASE_URL}/contactus
    Wait Until Page Contains    Contact Us    ${TIMEOUT}
    Page Should Contain    Contact Us
    Go Back
    Page Should Contain    Register

TC010_Verify Search Functionality
    [Documentation]    Test search functionality with different terms
    [Tags]    smoke    search    functionality
    Go To    ${BASE_URL}
    # Test valid search
    Input Text    //input[@id='small-searchterms']    laptop
    Click Element    //button[contains(text(),'Search')]
    Wait Until Page Contains    laptop    ${TIMEOUT}
    Page Should Contain    laptop
    # Test empty search
    Go To    ${BASE_URL}
    Click Element    //button[contains(text(),'Search')]
    Wait Until Element Is Visible    //div[@class='search-results']    ${TIMEOUT}

*** Keywords ***
Setup Test Environment
    [Documentation]    Setup test environment before suite execution
    Create Directory    screenshots
    Create Directory    reports
    Log    Test environment setup completed

Teardown Test Environment
    [Documentation]    Cleanup after suite execution
    Log    Test environment teardown completed

Setup Browser
    [Documentation]    Setup browser for each test
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    0.1

Teardown Browser
    [Documentation]    Cleanup browser after each test
    Run Keyword If Test Failed    Take Screenshot On Failure    ${TEST_NAME}
    Close Browser
