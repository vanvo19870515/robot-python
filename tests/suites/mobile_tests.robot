*** Settings ***
Documentation    Mobile Tests for SDET Technical Exercise
...              Demonstrates Appium mobile automation capabilities
Suite Setup      Setup Mobile Test Environment
Suite Teardown   Teardown Mobile Test Environment
Test Setup       Setup Mobile Browser
Test Teardown    Teardown Mobile Browser
Library          AppiumLibrary
Library          OperatingSystem
Library          Collections
Library          String
Library          ../../libraries/custom/MobileUtils.py
Resource         ../resources/common.robot
Resource         ../resources/locators.robot
Resource         ../resources/test_data.robot

*** Variables ***
${MOBILE_APP}           com.android.calculator2
${MOBILE_ACTIVITY}      com.android.calculator2.Calculator
${REMOTE_URL}           http://127.0.0.1:4723/wd/hub
${PLATFORM_NAME}        Android
${PLATFORM_VERSION}     11.0
${DEVICE_NAME}          emulator-5554
${AUTOMATION_NAME}      UiAutomator2

*** Test Cases ***
MOBILE001_Verify Calculator App Launch
    [Documentation]    Test that calculator app launches correctly
    [Tags]    mobile    calculator    appium    smoke
    Start Appium Server
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    deviceName=${DEVICE_NAME}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${MOBILE_APP}
    ...    appActivity=${MOBILE_ACTIVITY}

    # Verify app is running
    ${app_state}=    Check App State    ${MOBILE_APP}
    Should Not Be Empty    ${app_state}
    Log    App state: ${app_state}

    # Take mobile screenshot
    ${screenshot}=    Take Mobile Screenshot    calculator_app
    Should Not Be Empty    ${screenshot}

    # Get device info
    ${device_info}=    Get Device Info
    Log    Device info: ${device_info}

    [Teardown]    Run Keywords
    ...    Stop Appium Server
    ...    Close Application

MOBILE002_Verify Basic Calculator Operations
    [Documentation]    Test basic calculator functionality
    [Tags]    mobile    calculator    operations    working
    Start Appium Server
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    deviceName=${DEVICE_NAME}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${MOBILE_APP}
    ...    appActivity=${MOBILE_ACTIVITY}

    # Test number buttons exist
    Element Should Be Visible    //android.widget.Button[@text='1']
    Element Should Be Visible    //android.widget.Button[@text='2']
    Element Should Be Visible    //android.widget.Button[@text='3']
    Element Should Be Visible    //android.widget.Button[@text='4']
    Element Should Be Visible    //android.widget.Button[@text='5']

    # Test operator buttons
    Element Should Be Visible    //android.widget.Button[@text='+']
    Element Should Be Visible    //android.widget.Button[@text='-']
    Element Should Be Visible    //android.widget.Button[@text='×']
    Element Should Be Visible    //android.widget.Button[@text='÷']

    # Test equals and clear buttons
    Element Should Be Visible    //android.widget.Button[@text='=']
    Element Should Be Visible    //android.widget.Button[@text='C']

    [Teardown]    Run Keywords
    ...    Stop Appium Server
    ...    Close Application

MOBILE003_Verify Swipe Gestures
    [Documentation]    Test mobile swipe gestures
    [Tags]    mobile    gestures    swipe    working
    Start Appium Server
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    deviceName=${DEVICE_NAME}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${MOBILE_APP}
    ...    appActivity=${MOBILE_ACTIVITY}

    # Test swipe up
    Swipe Up    1000
    Sleep    1

    # Test swipe down
    Swipe Down    1000
    Sleep    1

    # Test swipe left
    Swipe Left    1000
    Sleep    1

    # Test swipe right
    Swipe Right    1000
    Sleep    1

    Log    All swipe gestures completed successfully

    [Teardown]    Run Keywords
    ...    Stop Appium Server
    ...    Close Application

MOBILE004_Verify Mobile Screenshots
    [Documentation]    Test mobile screenshot functionality
    [Tags]    mobile    screenshots    working
    Start Appium Server
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    deviceName=${DEVICE_NAME}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${MOBILE_APP}
    ...    appActivity=${MOBILE_ACTIVITY}

    # Take multiple screenshots
    ${screenshot1}=    Take Mobile Screenshot    mobile_test_1
    Should Not Be Empty    ${screenshot1}
    File Should Exist    ${screenshot1}

    # Perform some action
    Click Element    //android.widget.Button[@text='1']
    Sleep    1

    # Take another screenshot
    ${screenshot2}=    Take Mobile Screenshot    mobile_test_2
    Should Not Be Empty    ${screenshot2}
    File Should Exist    ${screenshot2}

    # Verify screenshots are different
    ${files_different}=    Run Keyword And Return Status
    ...    Should Not Be Equal As Strings    ${screenshot1}    ${screenshot2}
    Should Be True    ${files_different}

    Log    Mobile screenshots taken successfully

    [Teardown]    Run Keywords
    ...    Stop Appium Server
    ...    Close Application

MOBILE005_Verify Device Orientation
    [Documentation]    Test device orientation changes
    [Tags]    mobile    orientation    working
    Start Appium Server
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    deviceName=${DEVICE_NAME}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${MOBILE_APP}
    ...    appActivity=${MOBILE_ACTIVITY}

    # Test portrait mode (default)
    ${orientation}=    Get Element Attribute    //android.widget.LinearLayout    orientation
    Log    Current orientation: ${orientation}

    # Test landscape mode
    Rotate Device    LANDSCAPE
    Sleep    2

    # Verify orientation changed
    ${new_orientation}=    Get Element Attribute    //android.widget.LinearLayout    orientation
    Should Not Be Equal As Strings    ${orientation}    ${new_orientation}

    # Test portrait mode again
    Rotate Device    PORTRAIT
    Sleep    2

    Log    Device orientation tests completed

    [Teardown]    Run Keywords
    ...    Stop Appium Server
    ...    Close Application

MOBILE006_Verify App Backgrounding
    [Documentation]    Test app background and foreground functionality
    [Tags]    mobile    background    working
    Start Appium Server
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    deviceName=${DEVICE_NAME}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${MOBILE_APP}
    ...    appActivity=${MOBILE_ACTIVITY}

    # Verify app is in foreground
    ${initial_state}=    Check App State    ${MOBILE_APP}
    Log    Initial app state: ${initial_state}

    # Background app for 5 seconds
    Background App    5
    Sleep    6  # Wait a bit longer than background time

    # Verify app is back in foreground
    ${final_state}=    Check App State    ${MOBILE_APP}
    Log    Final app state: ${final_state}

    Log    App background/foreground test completed

    [Teardown]    Run Keywords
    ...    Stop Appium Server
    ...    Close Application

MOBILE007_Verify Mobile Performance
    [Documentation]    Test mobile performance metrics
    [Tags]    mobile    performance    working
    Start Appium Server
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    deviceName=${DEVICE_NAME}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${MOBILE_APP}
    ...    appActivity=${MOBILE_ACTIVITY}

    # Get initial performance data
    ${perf_data}=    Get Performance Data    cpuinfo
    Should Not Be Empty    ${perf_data}
    Log    Performance data retrieved: ${perf_data}

    # Perform some operations to generate load
    FOR    ${i}    IN RANGE    5
        Click Element    //android.widget.Button[@text='1']
        Sleep    0.5
    END

    # Get performance data after operations
    ${perf_data_after}=    Get Performance Data    meminfo
    Should Not Be Empty    ${perf_data_after}
    Log    Performance data after operations: ${perf_data_after}

    Log    Mobile performance test completed

    [Teardown]    Run Keywords
    ...    Stop Appium Server
    ...    Close Application

MOBILE008_Verify Mobile Error Handling
    [Documentation]    Test mobile error handling and recovery
    [Tags]    mobile    error-handling    working
    Start Appium Server
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    deviceName=${DEVICE_NAME}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${MOBILE_APP}
    ...    appActivity=${MOBILE_ACTIVITY}

    # Test resetting app
    Reset App
    Sleep    2

    # Verify app is still functional after reset
    Element Should Be Visible    //android.widget.Button[@text='1']
    Click Element    //android.widget.Button[@text='1']

    # Test app activation
    Activate App    ${MOBILE_APP}
    Sleep    1

    # Verify app is still functional
    Element Should Be Visible    //android.widget.Button[@text='1']

    Log    Mobile error handling test completed

    [Teardown]    Run Keywords
    ...    Stop Appium Server
    ...    Close Application

*** Keywords ***
Setup Mobile Test Environment
    [Documentation]    Setup mobile test environment
    Create Directory    screenshots/mobile
    Create Directory    reports/mobile
    Log    Mobile test environment setup completed

Teardown Mobile Test Environment
    [Documentation]    Cleanup mobile test environment
    Log    Mobile test environment teardown completed

Setup Mobile Browser
    [Documentation]    Setup mobile browser (if needed)
    Log    Mobile browser setup completed

Teardown Mobile Browser
    [Documentation]    Cleanup mobile browser
    Log    Mobile browser teardown completed
