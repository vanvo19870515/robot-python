*** Settings ***
Documentation    Common resources and keywords for all tests
Library          OperatingSystem
Library          Collections
Library          String
Library          DateTime

*** Variables ***
${BROWSER}              chrome
${HEADLESS_BROWSER}     ${False}
${TIMEOUT}              10
${DELAY}                0.1
${SCREENSHOT_DIR}       screenshots
${REPORTS_DIR}          reports
${TEMP_DIR}             temp

*** Keywords ***
Setup Test Environment
    [Documentation]    Setup test environment before suite execution
    Create Directory    ${SCREENSHOT_DIR}
    Create Directory    ${REPORTS_DIR}
    Create Directory    ${TEMP_DIR}
    Log    Test environment setup completed

Teardown Test Environment
    [Documentation]    Cleanup after suite execution
    Log    Test environment teardown completed

Setup Browser
    [Documentation]    Setup browser for each test
    [Arguments]    ${url}=https://demo.nopcommerce.com
    Open Browser    ${url}    ${BROWSER}
    Set Selenium Timeout    ${TIMEOUT}
    Set Selenium Speed    ${DELAY}
    Maximize Browser Window

Teardown Browser
    [Documentation]    Cleanup browser after each test
    [Arguments]    ${take_screenshot}=${True}
    Run Keyword If    ${take_screenshot}    Take Screenshot On Failure    ${TEST_NAME}
    Close Browser

Take Screenshot On Failure
    [Documentation]    Take screenshot when test fails
    [Arguments]    ${test_name}
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${filename}=    Set Variable    ${test_name}_${timestamp}_FAILED.png
    ${filepath}=    Set Variable    ${SCREENSHOT_DIR}/${filename}
    Capture Page Screenshot    ${filepath}
    Log    Screenshot saved: ${filepath}

Generate Random Email
    [Documentation]    Generate a random email for testing
    ${random_string}=    Generate Random String    8    [LOWER]
    ${email}=    Set Variable    test_${random_string}@example.com
    RETURN    ${email}

Generate Random String
    [Documentation]    Generate random string of specified length
    [Arguments]    ${length}=8    ${chars}=[LETTERS][DIGITS]
    ${random_string}=    Evaluate    ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(${length}))    modules=random,string
    RETURN    ${random_string}

Wait And Click Element
    [Documentation]    Wait for element to be clickable and click it
    [Arguments]    ${locator}    ${timeout}=10
    Wait Until Element Is Visible    ${locator}    ${timeout}
    Wait Until Element Is Enabled    ${locator}    ${timeout}
    Click Element    ${locator}

Wait For Element To Be Visible
    [Documentation]    Wait for element to be visible
    [Arguments]    ${locator}    ${timeout}=10
    Wait Until Element Is Visible    ${locator}    ${timeout}

Clear And Type Text
    [Documentation]    Clear field and type new text
    [Arguments]    ${locator}    ${text}
    Clear Element Text    ${locator}
    Input Text    ${locator}    ${text}

Select Dropdown By Text
    [Documentation]    Select dropdown option by visible text
    [Arguments]    ${locator}    ${text}
    Select From List By Label    ${locator}    ${text}

Verify Page Contains
    [Documentation]    Verify page contains specific text
    [Arguments]    ${text}
    Page Should Contain    ${text}

Verify Element Text
    [Documentation]    Verify element contains specific text
    [Arguments]    ${locator}    ${expected_text}
    Element Should Contain    ${locator}    ${expected_text}

Verify Element Is Visible
    [Documentation]    Verify element is visible
    [Arguments]    ${locator}
    Element Should Be Visible    ${locator}

Verify Element Is Enabled
    [Documentation]    Verify element is enabled
    [Arguments]    ${locator}
    Element Should Be Enabled    ${locator}

Log Test Information
    [Documentation]    Log test information for debugging
    [Arguments]    ${message}
    Log    ${message}
    Log To Console    ${message}
