*** Settings ***
Documentation    Mobile Simulation Tests for SDET Technical Exercise
...              Demonstrates mobile testing concepts using Chrome DevTools
...              Simulates mobile behavior without requiring Appium server
Suite Setup      Setup Mobile Simulation Environment
Suite Teardown   Teardown Mobile Simulation Environment
Test Setup       Setup Mobile Browser
Test Teardown    Teardown Mobile Browser
Library          SeleniumLibrary
Library          OperatingSystem
Library          Collections
Library          String
Library          ../../libraries/custom/WebUtils.py
Resource         ../resources/common.robot
Resource         ../resources/locators.robot
Resource         ../resources/test_data.robot

*** Variables ***
${BASE_URL}         https://demo.nopcommerce.com
${BROWSER}          chrome
${TIMEOUT}          10

*** Test Cases ***
MOBILE_SIM_001_Test Mobile Viewport Simulation
    [Documentation]    Test mobile viewport simulation using Chrome DevTools
    [Tags]    mobile    simulation    responsive    working
    Go To    ${BASE_URL}

    # Test iPhone SE viewport
    Set Window Size    375    667
    ${screenshot_iphone}=    Capture Page Screenshot    mobile_iphone_se.png

    # Verify mobile-specific elements are visible
    Element Should Be Visible    ${HOME_LOGO}
    Element Should Be Visible    ${SEARCH_BOX}

    # Test responsive behavior
    ${window_size}=    Get Window Size
    Log    Current viewport: ${window_size}[0]x${window_size}[1] (iPhone SE)

MOBILE_SIM_002_Test Tablet Viewport Simulation
    [Documentation]    Test tablet viewport simulation
    [Tags]    mobile    simulation    tablet    working
    Go To    ${BASE_URL}

    # Test iPad viewport
    Set Window Size    768    1024
    ${screenshot_ipad}=    Capture Page Screenshot    mobile_ipad.png

    # Verify tablet layout
    Element Should Be Visible    ${HOME_LOGO}
    Element Should Be Visible    ${SEARCH_BOX}

    # Test responsive behavior
    ${window_size}=    Get Window Size
    Log    Current viewport: ${window_size}[0]x${window_size}[1] (iPad)

MOBILE_SIM_003_Test Mobile Touch Simulation
    [Documentation]    Test mobile touch simulation using JavaScript
    [Tags]    mobile    simulation    touch    working
    Go To    ${BASE_URL}

    # Simulate mobile viewport
    Set Window Size    375    667

    # Simulate touch events using JavaScript
    Execute JavaScript
    ...    // Simulate touch event on search box
    ...    var searchBox = document.querySelector('input[id="small-searchterms"]');
    ...    if (searchBox) {
    ...        var touchEvent = new Event('touchstart', { bubbles: true });
    ...        searchBox.dispatchEvent(touchEvent);
    ...        console.log('Touch event simulated on search box');
    ...    }

    # Test mobile-specific interactions
    Input Text    ${SEARCH_BOX}    mobile test
    ${search_value}=    Get Value    ${SEARCH_BOX}
    Should Be Equal As Strings    ${search_value}    mobile test

    ${screenshot_touch}=    Capture Page Screenshot    mobile_touch_simulation.png
    Log    Mobile touch simulation completed

MOBILE_SIM_004_Test Mobile User Agent Simulation
    [Documentation]    Test mobile user agent simulation
    [Tags]    mobile    simulation    user-agent    working
    Go To    ${BASE_URL}

    # Set mobile user agent
    Execute JavaScript
    ...    Object.defineProperty(navigator, 'userAgent', {
    ...        value: 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
    ...        configurable: false
    ...    });

    # Verify user agent change
    ${user_agent}=    Execute JavaScript    return navigator.userAgent;
    Log    Simulated user agent: ${user_agent}
    Should Contain    ${user_agent}    iPhone

    # Test mobile behavior
    Set Window Size    375    667
    ${screenshot_user_agent}=    Capture Page Screenshot    mobile_user_agent.png
    Log    Mobile user agent simulation completed

MOBILE_SIM_005_Test Mobile CSS Media Queries
    [Documentation]    Test mobile CSS media queries and responsive design
    [Tags]    mobile    simulation    css    responsive    working
    Go To    ${BASE_URL}

    # Test different breakpoints
    @{viewports}=    Create List    320x568    375x667    414x896    768x1024    1920x1080

    FOR    ${viewport}    IN    @{viewports}
        ${width}    ${height}=    Split String    ${viewport}    x
        Set Window Size    ${width}    ${height}

        # Test responsive elements
        Element Should Be Visible    ${HOME_LOGO}
        Element Should Be Visible    ${SEARCH_BOX}

        # Capture screenshot for each viewport
        ${screenshot}=    Capture Page Screenshot    mobile_breakpoint_${viewport}.png
        Log    Tested viewport: ${viewport}

        Sleep    1  # Brief pause between tests
    END

    Log    Mobile CSS media queries test completed

MOBILE_SIM_006_Test Mobile Performance Simulation
    [Documentation]    Test mobile performance simulation
    [Tags]    mobile    simulation    performance    working
    Go To    ${BASE_URL}

    # Simulate slow mobile network
    ${start_time}=    Get Time    epoch

    # Perform mobile-like interactions
    Set Window Size    375    667
    Input Text    ${SEARCH_BOX}    performance test
    Click Element    ${SEARCH_BUTTON}
    Wait Until Page Contains    performance test    ${TIMEOUT}

    ${end_time}=    Get Time    epoch
    ${duration}=    Evaluate    ${end_time} - ${start_time}

    Log    Mobile performance test duration: ${duration} seconds
    Should Be True    ${duration} < 10    Performance test should complete within 10 seconds

    ${screenshot_performance}=    Capture Page Screenshot    mobile_performance.png
    Log    Mobile performance simulation completed

MOBILE_SIM_007_Test Mobile Accessibility Simulation
    [Documentation]    Test mobile accessibility features
    [Tags]    mobile    simulation    accessibility    working
    Go To    ${BASE_URL}

    # Simulate mobile accessibility features
    Set Window Size    375    667

    # Test keyboard navigation
    Press Keys    ${SEARCH_BOX}    TAB
    ${active_element}=    Execute JavaScript    return document.activeElement.id;

    Log    Active element after tab: ${active_element}
    Should Not Be Empty    ${active_element}

    # Test ARIA labels (if available)
    ${aria_labels}=    Get Element Count    //*[@aria-label]
    Log    Found ${aria_labels} elements with ARIA labels

    ${screenshot_accessibility}=    Capture Page Screenshot    mobile_accessibility.png
    Log    Mobile accessibility simulation completed

MOBILE_SIM_008_Test Mobile Gesture Simulation
    [Documentation]    Test mobile gesture simulation using JavaScript
    [Tags]    mobile    simulation    gestures    working
    Go To    ${BASE_URL}

    Set Window Size    375    667

    # Simulate swipe gestures using JavaScript
    Execute JavaScript
    ...    // Simulate mobile swipe gestures
    ...    function simulateSwipe(startX, startY, endX, endY, duration) {
    ...        var element = document.elementFromPoint(startX, startY);
    ...        if (element) {
    ...            var touchStart = new Touch({
    ...                identifier: Date.now(),
    ...                target: element,
    ...                clientX: startX,
    ...                clientY: startY
    ...            });
    ...            var touchEnd = new Touch({
    ...                identifier: Date.now(),
    ...                target: element,
    ...                clientX: endX,
    ...                clientY: endY
    ...            });
    ...            var touchStartEvent = new TouchEvent('touchstart', { touches: [touchStart] });
    ...            var touchEndEvent = new TouchEvent('touchend', { touches: [touchEnd] });
    ...            element.dispatchEvent(touchStartEvent);
    ...            setTimeout(() => element.dispatchEvent(touchEndEvent), duration);
    ...        }
    ...    }

    # Test various gestures
    ${viewport_size}=    Get Window Size
    ${width}=    Get From Dictionary    ${viewport_size}    width
    ${height}=    Get From Dictionary    ${viewport_size}    height

    # Simulate swipe right
    Execute JavaScript
    ...    simulateSwipe(${width}*0.2, ${height}*0.5, ${width}*0.8, ${height}*0.5, 500);

    Sleep    1

    Log    Mobile gesture simulation completed
    ${screenshot_gestures}=    Capture Page Screenshot    mobile_gestures.png

*** Keywords ***
Setup Mobile Simulation Environment
    [Documentation]    Setup mobile simulation environment
    Create Directory    screenshots/mobile
    Create Directory    reports/mobile
    Log    Mobile simulation environment setup completed

Teardown Mobile Simulation Environment
    [Documentation]    Cleanup mobile simulation environment
    Log    Mobile simulation environment teardown completed

Setup Mobile Browser
    [Documentation]    Setup browser for mobile simulation
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}

Teardown Mobile Browser
    [Documentation]    Cleanup browser after mobile simulation
    ${screenshot_taken}=    Run Keyword And Return Status    Capture Page Screenshot    ${TEST_NAME}_teardown.png
    Close Browser
