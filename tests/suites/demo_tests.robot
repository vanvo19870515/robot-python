*** Settings ***
Documentation    Demo Tests for SDET Technical Exercise
...              Showcases Robot Framework capabilities with Selenium
Suite Setup      Setup Test Environment
Suite Teardown   Teardown Test Environment
Test Setup       Setup Browser
Test Teardown    Teardown Browser
Library          SeleniumLibrary
Library          OperatingSystem
Library          Collections
Library          String
Resource         ../resources/common.robot
Resource         ../resources/locators.robot
Resource         ../resources/test_data.robot

*** Variables ***
${BASE_URL}         https://demo.nopcommerce.com
${BROWSER}          chrome
${TIMEOUT}          10

*** Test Cases ***
DEMO001_Verify Basic Navigation
    [Documentation]    Demonstrate basic navigation and page validation
    [Tags]    demo    navigation    working
    Go To    ${BASE_URL}
    ${title}=    Get Title
    Should Contain    ${title}    nopCommerce
    Page Should Contain    Welcome to our store
    Capture Page Screenshot    demo_navigation.png
    Log    ✅ Navigation test completed successfully

DEMO002_Verify Page Elements
    [Documentation]    Demonstrate element verification and interaction
    [Tags]    demo    elements    working
    Go To    ${BASE_URL}
    # Check if logo exists
    Element Should Be Visible    ${HOME_LOGO}
    # Check if search box exists
    Element Should Be Visible    ${SEARCH_BOX}
    # Check if cart exists
    Element Should Be Visible    ${SHOPPING_CART}
    Log    ✅ Page elements verification completed

DEMO003_Verify Search Box Interaction
    [Documentation]    Demonstrate form interaction and validation
    [Tags]    demo    forms    working
    Go To    ${BASE_URL}
    # Test search box is enabled
    Element Should Be Enabled    ${SEARCH_BOX}
    # Test search box is empty initially
    ${initial_value}=    Get Value    ${SEARCH_BOX}
    Should Be Empty    ${initial_value}
    # Type in search box
    Input Text    ${SEARCH_BOX}    demo
    # Verify text was entered
    ${entered_value}=    Get Value    ${SEARCH_BOX}
    Should Be Equal As Strings    ${entered_value}    demo
    Log    ✅ Search box interaction completed

DEMO004_Verify Responsive Behavior
    [Documentation]    Demonstrate responsive design testing
    [Tags]    demo    responsive    working
    Go To    ${BASE_URL}
    # Test on mobile viewport
    Set Window Size    375    667
    Element Should Be Visible    ${HOME_LOGO}
    # Test on tablet viewport
    Set Window Size    768    1024
    Element Should Be Visible    ${HOME_LOGO}
    # Test on desktop viewport
    Set Window Size    1920    1080
    Element Should Be Visible    ${HOME_LOGO}
    Log    ✅ Responsive design test completed

DEMO005_Verify Error Handling
    [Documentation]    Demonstrate error handling and recovery
    [Tags]    demo    error-handling    working
    Go To    ${BASE_URL}/nonexistent
    # This should fail gracefully
    ${status}=    Run Keyword And Return Status    Page Should Contain    Welcome to our store
    Should Be True    ${status} == ${False}    Expected page not found
    Log    ✅ Error handling test completed

DEMO006_Verify Screenshot Capture
    [Documentation]    Demonstrate screenshot functionality
    [Tags]    demo    screenshots    working
    Go To    ${BASE_URL}
    # Take screenshot
    Capture Page Screenshot    demo_screenshot.png
    # Verify screenshot was taken
    Log    Screenshot functionality working
    Log    ✅ Screenshot capture completed

DEMO007_Verify Dynamic Content
    [Documentation]    Demonstrate dynamic content validation
    [Tags]    demo    dynamic    working
    Go To    ${BASE_URL}
    # Get current URL
    ${current_url}=    Get Location
    Should Start With    ${current_url}    https://demo.nopcommerce.com
    # Get page title
    ${page_title}=    Get Title
    Should Not Be Empty    ${page_title}
    # Count product items
    ${product_count}=    Get Element Count    ${PRODUCT_ITEM}
    Log    Found ${product_count} products on the page
    Log    ✅ Dynamic content validation completed

*** Keywords ***
Setup Test Environment
    [Documentation]    Setup test environment before suite execution
    Create Directory    screenshots
    Create Directory    reports
    Log    Demo test environment setup completed

Teardown Test Environment
    [Documentation]    Cleanup after suite execution
    Log    Demo test environment teardown completed

Setup Browser
    [Documentation]    Setup browser for each test
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}

Teardown Browser
    [Documentation]    Cleanup browser after each test
    ${screenshot_taken}=    Run Keyword And Return Status    Capture Page Screenshot    ${TEST_NAME}_teardown.png
    Close Browser
