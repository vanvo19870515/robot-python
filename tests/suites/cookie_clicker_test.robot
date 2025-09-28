*** Settings ***
Documentation     Comprehensive test suite for Cookie Clicker game
...               Tests basic gameplay, visual validation, and reporting
Library           SeleniumLibrary
Library           String

*** Variables ***
${GAME_URL}                 https://orteil.dashnet.org/cookieclicker/
${BROWSER}                  Chrome
${COOKIE_LOCATOR}           id:bigCookie
${SCORE_LOCATOR}            id:cookies
${CURSOR_UPGRADE}           id:product0

# Test Configuration
${VIEWPORT_WIDTH}           1920
${VIEWPORT_HEIGHT}          1080

*** Test Cases ***
Test Cookie Clicker Basic Gameplay
    [Documentation]    Basic test of Cookie Clicker core functionality
    [Tags]    web    cookie-clicker

    # Setup
    Setup Test Environment

    # Open game and test basic functionality
    Open Cookie Clicker Game
    Handle Language Selection And Consent
    Perform Initial Cookie Clicks
    Verify Score Increased
    Purchase First Upgrade
    Verify Upgrade Purchase

    [Teardown]    Cleanup Test Environment

*** Keywords ***
Setup Test Environment
    [Documentation]    Initialize test environment and browser
    Open Browser    ${GAME_URL}    ${BROWSER}
    Set Window Size    ${VIEWPORT_WIDTH}    ${VIEWPORT_HEIGHT}
    Set Browser Implicit Wait    10s

Open Cookie Clicker Game
    [Documentation]    Open the Cookie Clicker game and wait for it to load
    Wait Until Element Is Visible    ${COOKIE_LOCATOR}    timeout=60s
    Log    Cookie Clicker game loaded successfully

Handle Language Selection And Consent
    [Documentation]    Handle initial popups if they appear
    Log    Handling initial popups if they appear...

    # Language Selection (wait a bit for it to appear)
    Sleep    2s
    ${lang_select_visible}=    Run Keyword And Return Status    Page Should Contain Element    id:langSelect-EN
    Run Keyword If    ${lang_select_visible}    Click Element    id:langSelect-EN

    # GDPR Consent
    Sleep    1s
    ${consent_visible}=    Run Keyword And Return Status    Page Should Contain Element    //button[text()='Got it!']
    Run Keyword If    ${consent_visible}    Click Element    //button[text()='Got it!']

    Sleep    2s    # Wait for any remaining loading


Perform Initial Cookie Clicks
    [Documentation]    Click the big cookie multiple times to generate cookies
    Log    Clicking the big cookie 15 times...

    FOR    ${i}    IN RANGE    15
        Click Element    ${COOKIE_LOCATOR}
        Sleep    0.1s    # Small delay between clicks
    END

    Sleep    1s    # Wait for score to update

Verify Score Increased
    [Documentation]    Verify that the score has increased after clicking
    Log    Verifying the score has updated...

    ${score_text}=    Get Text    ${SCORE_LOCATOR}
    ${score_value}=    Get Regexp Matches    ${score_text}    \\d+
    ${score_number}=    Convert To Integer    ${score_value[0]}

    Should Be True    ${score_number} >= 15    The score should be at least 15, but was ${score_number}

    Log    Score verification passed: ${score_number} cookies

Purchase First Upgrade
    [Documentation]    Purchase the first upgrade (Cursor) when available
    Log    Attempting to buy the "Cursor" upgrade...

    Wait Until Element Is Enabled    ${CURSOR_UPGRADE}    timeout=30s
    Click Element    ${CURSOR_UPGRADE}
    Sleep    1s

Verify Upgrade Purchase
    [Documentation]    Verify that the upgrade was purchased and score was deducted
    Log    Verifying the score was deducted and cursor is owned...

    ${score_text}=    Get Text    ${SCORE_LOCATOR}
    ${score_value}=    Get Regexp Matches    ${score_text}    \\d+
    ${score_number}=    Convert To Integer    ${score_value[0]}

    Should Be True    ${score_number} < 15    Score should be less than 15 after purchase, but was ${score_number}

    ${cursor_owned}=    Get Text    id:productOwned0
    ${cursor_count}=    Convert To Integer    ${cursor_owned}
    Should Be Equal As Integers    ${cursor_count}    1    Should own 1 cursor, but found ${cursor_count}

    # Send upgrade notification
    Log    Upgrade purchase verification passed


Cleanup Test Environment
    [Documentation]    Clean up test environment
    Close Browser

    # Send final test summary
    Log    Cookie Clicker test completed successfully
