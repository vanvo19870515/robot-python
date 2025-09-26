*** Settings ***
Documentation    Appium Setup Validation Tests
...              Validates that Appium is properly configured and ready for mobile testing
Suite Setup      Setup Appium Validation
Suite Teardown   Teardown Appium Validation
Test Setup       Setup Validation
Test Teardown    Teardown Validation
Library          OperatingSystem
Library          Process
Resource         ../resources/common.robot

*** Variables ***
${APPIUM_HOST}      127.0.0.1
${APPIUM_PORT}      4723

*** Test Cases ***
APPIUM_001_Validate Appium Installation
    [Documentation]    Test that Appium is properly installed and accessible
    [Tags]    appium    validation    setup    working
    ${appium_version}=    Run Process    appium --version    shell=True
    Should Be Equal As Integers    ${appium_version.rc}    0
    Should Not Be Empty    ${appium_version.stdout}
    Log    Appium version: ${appium_version.stdout}

APPIUM_002_Validate Appium Server Startup
    [Documentation]    Test that Appium server can start successfully
    [Tags]    appium    server    startup    working
    ${appium_process}=    Start Process    appium --port ${APPIUM_PORT} --log-level info
    ...    shell=True    alias=appium_server
    Sleep    3

    # Check if server is running
    ${result}=    Run Process    curl -s http://localhost:${APPIUM_PORT}/wd/hub/status    shell=True
    Should Contain    ${result.stdout}    "ready"
    Should Contain    ${result.stdout}    "message"

    # Stop the server
    Terminate Process    ${appium_process}
    Sleep    2
    Log    Appium server started and stopped successfully

APPIUM_003_Validate MobileUtils Library
    [Documentation]    Test that MobileUtils library loads correctly
    [Tags]    appium    library    mobileutils    working
    ${mobile_utils_loaded}=    Run Keyword And Return Status
    ...    Import Library    ../../libraries/custom/MobileUtils.py
    Should Be True    ${mobile_utils_loaded}
    Log    MobileUtils library loaded successfully

APPIUM_004_Validate Appium Configuration
    [Documentation]    Test that Appium configuration files are valid
    [Tags]    appium    configuration    yaml    working
    File Should Exist    config/appium.yaml
    ${config_size}=    Get File Size    config/appium.yaml
    Should Be True    ${config_size} > 100    # At least 100 bytes
    Log    Appium configuration file is valid (size: ${config_size} bytes)

APPIUM_005_Validate UiAutomator2 Driver
    [Documentation]    Test that UiAutomator2 driver is installed
    [Tags]    appium    driver    uiautomator2    working
    ${driver_check}=    Run Process    appium driver list    shell=True
    Should Be Equal As Integers    ${driver_check.rc}    0
    Should Contain    ${driver_check.stdout}    uiautomator2
    Log    UiAutomator2 driver is available: ${driver_check.stdout}

APPIUM_006_Validate Mobile Test Files
    [Documentation]    Test that mobile test files are properly structured
    [Tags]    appium    tests    structure    working
    File Should Exist    tests/suites/mobile_tests.robot
    File Should Exist    tests/suites/mobile_simulation_tests.robot

    # Check test counts
    ${mobile_tests}=    Grep File    tests/suites/mobile_tests.robot    MOBILE\\d+
    ${simulation_tests}=    Grep File    tests/suites/mobile_simulation_tests.robot    MOBILE_SIM_\\d+
    Log    Mobile tests found: ${mobile_tests}
    Log    Simulation tests found: ${simulation_tests}

APPIUM_007_Validate Environment Variables
    [Documentation]    Test environment variables for mobile testing
    [Tags]    appium    environment    variables    working
    ${path_set}=    Run Keyword And Return Status    Environment Variable Should Be Set    PATH
    Should Be True    ${path_set}

    # Check if Appium is in PATH
    ${appium_in_path}=    Run Process    which appium    shell=True
    Should Be Equal As Integers    ${appium_in_path.rc}    0
    Log    Appium is available in PATH

APPIUM_008_Validate Mobile Test Capabilities
    [Documentation]    Test that mobile test capabilities are properly configured
    [Tags]    appium    capabilities    configuration    working
    ${appium_config}=    Get File    config/appium.yaml
    Should Contain    ${appium_config}    platform_name: "Android"
    Should Contain    ${appium_config}    automation_name: "UiAutomator2"
    Should Contain    ${appium_config}    app_package: "com.android.calculator2"
    Log    Mobile test capabilities are properly configured

*** Keywords ***
Setup Appium Validation
    [Documentation]    Setup Appium validation environment
    Create Directory    reports/appium
    Log    Appium validation environment setup completed

Teardown Appium Validation
    [Documentation]    Cleanup Appium validation environment
    ${appium_running}=    Run Keyword And Return Status    Process Should Be Running    appium_server
    Run Keyword If    ${appium_running}    Terminate All Processes
    Log    Appium validation environment teardown completed

Setup Validation
    [Documentation]    Setup for individual validation tests
    Log    Validation test setup completed

Teardown Validation
    [Documentation]    Cleanup after validation tests
    Log    Validation test teardown completed
