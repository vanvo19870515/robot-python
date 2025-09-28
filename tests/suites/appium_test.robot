*** Settings ***
Documentation     Simple Appium test to verify connection
Library           AppiumLibrary

*** Variables ***
${APPIUM_SERVER}    http://127.0.0.1:4723/wd/hub
${PLATFORM_NAME}    Android
${DEVICE_NAME}      Android Emulator
${AUTOMATION_NAME}  UiAutomator2

*** Test Cases ***
Test Appium Connection
    [Documentation]    Simple test to verify Appium connection works
    Open Application    ${APPIUM_SERVER}
    ...                 platformName=${PLATFORM_NAME}
    ...                 deviceName=${DEVICE_NAME}
    ...                 automationName=${AUTOMATION_NAME}
    ...                 app=${EXECDIR}/apps/ApiDemos-debug.apk

    # Simple test - check if app opens
    Wait Until Page Contains Element    id=android:id/content    timeout=30s

    # Take a screenshot
    Capture Page Screenshot

    [Teardown]    Close Application