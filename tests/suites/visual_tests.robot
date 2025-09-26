*** Settings ***
Documentation    Visual Tests for SDET Technical Exercise
...              Demonstrates Applitools Eyes visual testing with Allure integration
Suite Setup      Setup Visual Test Environment
Suite Teardown   Teardown Visual Test Environment
Test Setup       Setup Browser
Test Teardown    Teardown Browser
Library          SeleniumLibrary
Library          OperatingSystem
Library          Collections
Library          String
Library          ../../libraries/ai/AIVisualValidator.py
Library          ../../libraries/ai/ApplitoolsValidator.py
Resource         ../resources/common.robot
Resource         ../resources/locators.robot
Resource         ../resources/test_data.robot

*** Variables ***
${BASE_URL}         https://demo.nopcommerce.com
${BROWSER}          chrome
${TIMEOUT}          10
${APPLITOOLS_API_KEY}    ${EMPTY}  # Set your API key

*** Test Cases ***
VISUAL001_Verify Home Page Visual Baseline
    [Documentation]    Create visual baseline for home page
    [Tags]    visual    baseline    applitools    working
    Start Visual Test    Home Page Baseline    1920x1080
    Go To    ${BASE_URL}
    Wait Until Page Contains    nopCommerce    ${TIMEOUT}

    # Check main window
    Check Window    Home Page Main View

    # Check specific elements
    Check Element    ${HOME_LOGO}    Logo Element
    Check Element    ${SEARCH_BOX}    Search Box Element

    # End visual test
    ${result}=    End Visual Test
    Should Not Be Empty    ${result}
    Log    Visual test result: ${result}

VISUAL002_Verify Product Search Visual Elements
    [Documentation]    Test visual elements during product search
    [Tags]    visual    search    applitools    working
    Start Visual Test    Product Search Test    1920x1080
    Go To    ${BASE_URL}

    # Take initial screenshot
    ${baseline}=    Capture Page Screenshot    visual_search_baseline

    # Perform search
    Input Text    ${SEARCH_BOX}    laptop
    Click Element    ${SEARCH_BUTTON}
    Wait Until Page Contains    laptop    ${TIMEOUT}

    # Check search results page
    Check Window    Search Results Page

    # Check specific search elements
    Check Element    //div[@class='product-grid']    Product Grid
    Check Element    //div[@class='search-results']    Search Results

    # Take current screenshot
    ${current}=    Capture Page Screenshot    visual_search_current

    # Compare images
    ${is_similar}    ${score}=    Compare Baseline Images    ${baseline}    ${current}    0.95
    Log    Visual similarity: ${score:.2%}

    # End visual test
    ${result}=    End Visual Test
    Should Not Be Empty    ${result}
    Log    Visual test result: ${result}

VISUAL003_Verify Registration Form Visual Layout
    [Documentation]    Test registration form visual layout
    [Tags]    visual    forms    applitools    working
    Start Visual Test    Registration Form Test    1920x1080
    Go To    ${BASE_URL}/register

    # Check registration form
    Check Window    Registration Form Full Page

    # Check specific form sections
    Check Element    //form[@method='post']    Registration Form
    Check Element    //fieldset    Personal Details Section
    Check Element    //button[@id='register-button']    Register Button

    # Test form interaction
    Select Radio Button    gender    M
    Check Window    Registration Form After Gender Selection

    Input Text    ${REG_FIRST_NAME}    Test
    Input Text    ${REG_LAST_NAME}    User
    Check Window    Registration Form After Name Input

    # End visual test
    ${result}=    End Visual Test
    Should Not Be Empty    ${result}
    Log    Visual test result: ${result}

VISUAL004_Verify Responsive Visual Testing
    [Documentation]    Test visual elements across different screen sizes
    [Tags]    visual    responsive    applitools    working
    Start Visual Test    Responsive Design Test    1920x1080
    Go To    ${BASE_URL}

    # Test desktop view
    Set Window Size    1920    1080
    Check Window    Desktop View 1920x1080

    # Test tablet view
    Set Window Size    768    1024
    Check Window    Tablet View 768x1024

    # Test mobile view
    Set Window Size    375    667
    Check Window    Mobile View 375x667

    # End visual test
    ${result}=    End Visual Test
    Should Not Be Empty    ${result}
    Log    Visual test result: ${result}

VISUAL005_Verify Visual Consistency Validation
    [Documentation]    Test visual consistency with tolerance
    [Tags]    visual    consistency    applitools    working
    Go To    ${BASE_URL}

    # Take baseline screenshot
    ${baseline}=    Capture Page Screenshot    visual_consistency_baseline

    # Navigate to different page
    Go To    ${BASE_URL}/register
    ${current}=    Capture Page Screenshot    visual_consistency_current

    # Validate visual consistency
    ${consistency}=    Validate Visual Consistency    ${baseline}    ${current}    5
    Log    Visual consistency score: ${consistency}[consistency_score]%

    # Should be visually different (different pages)
    Should Be True    ${consistency}[is_consistent] == ${False}
    Log    Pages are visually different as expected

VISUAL006_Verify Applitools Screenshot Integration
    [Documentation]    Test Applitools screenshot functionality
    [Tags]    visual    screenshots    applitools    working
    Start Visual Test    Screenshot Integration Test    1920x1080
    Go To    ${BASE_URL}

    # Take regular screenshot
    ${regular_screenshot}=    Capture Page Screenshot    regular_screenshot

    # Take Applitools screenshot
    ${applitools_screenshot}=    Take Applitools Screenshot    applitools_screenshot
    Should Not Be Empty    ${applitools_screenshot}

    # Verify files exist
    File Should Exist    ${regular_screenshot}
    File Should Exist    ${applitools_screenshot}

    # Check window with Applitools
    Check Window    Full Page Screenshot

    # End visual test
    ${result}=    End Visual Test
    Should Not Be Empty    ${result}
    Log    Visual test result: ${result}

VISUAL007_Verify Visual Grid Cross-Browser Testing
    [Documentation]    Test visual grid for cross-browser compatibility
    [Tags]    visual    cross-browser    applitools    working
    Setup Visual Grid    3  # 3 concurrent browsers

    # Test home page across multiple browsers
    Start Visual Test    Cross Browser Test    1920x1080
    Go To    ${BASE_URL}
    Check Window    Home Page Cross Browser

    # Test search functionality across browsers
    Input Text    ${SEARCH_BOX}    test
    Click Element    ${SEARCH_BUTTON}
    Check Window    Search Results Cross Browser

    # End visual test
    ${result}=    End Visual Test
    Should Not Be Empty    ${result}
    Log    Visual test result: ${result}

VISUAL008_Verify Visual Report Generation
    [Documentation]    Test visual report generation
    [Tags]    visual    reporting    applitools    working
    Start Visual Test    Visual Report Test    1920x1080
    Go To    ${BASE_URL}

    # Perform various actions
    Check Window    Initial State
    Input Text    ${SEARCH_BOX}    report
    Check Window    After Search Input
    Click Element    ${SEARCH_BUTTON}
    Check Window    Search Results

    # End visual test
    ${result}=    End Visual Test
    Should Not Be Empty    ${result}

    # Generate comprehensive visual report
    ${report_path}=    Generate Visual Report    ${result}
    Should Not Be Empty    ${report_path}
    File Should Exist    ${report_path}

    Log    Visual report generated: ${report_path}

VISUAL009_Verify Image Quality Analysis
    [Documentation]    Test image quality analysis functionality
    [Tags]    visual    quality    working
    Go To    ${BASE_URL}

    # Take screenshot and analyze quality
    ${screenshot}=    Capture Page Screenshot    quality_test
    ${quality_metrics}=    Validate Image Quality    ${screenshot}

    Should Not Be Empty    ${quality_metrics}
    Log    Image quality metrics: ${quality_metrics}

    # Validate quality score
    ${quality_score}=    Get From Dictionary    ${quality_metrics}    quality_score
    Should Be True    ${quality_score} >= 50    Image quality should be acceptable

VISUAL010_Verify Element Visual Detection
    [Documentation]    Test AI-powered UI element detection
    [Tags]    visual    detection    ai    working
    Go To    ${BASE_URL}

    # Take screenshot for element detection
    ${screenshot}=    Capture Page Screenshot    element_detection_test
    ${elements}=    Detect UI Elements    ${screenshot}

    Should Not Be Empty    ${elements}
    Log    Detected ${elements}[total_elements] UI elements

    # Verify key elements were detected
    ${elements_list}=    Get From Dictionary    ${elements}    elements
    ${element_count}=    Get Length    ${elements_list}
    Should Be True    ${element_count} > 5    Should detect multiple UI elements

*** Keywords ***
Setup Visual Test Environment
    [Documentation]    Setup visual test environment
    Create Directory    screenshots/visual
    Create Directory    reports/visual
    # Set API key if available
    Run Keyword If    '${APPLITOOLS_API_KEY}' != '${EMPTY}'
    ...    Set Environment Variable    APPLITOOLS_API_KEY    ${APPLITOOLS_API_KEY}
    Log    Visual test environment setup completed

Teardown Visual Test Environment
    [Documentation]    Cleanup visual test environment
    Log    Visual test environment teardown completed

Setup Browser
    [Documentation]    Setup browser for visual tests
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}

Teardown Browser
    [Documentation]    Cleanup browser after visual tests
    ${screenshot_taken}=    Run Keyword And Return Status    Capture Page Screenshot    ${TEST_NAME}_teardown.png
    Close Browser
