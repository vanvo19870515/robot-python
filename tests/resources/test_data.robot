*** Variables ***
# Test Data for nopCommerce Demo Site

# User Credentials
${VALID_EMAIL}                  test@example.com
${VALID_PASSWORD}               TestPass123
${INVALID_EMAIL}                invalid@test.com
${INVALID_PASSWORD}             wrongpass

# User Information
${FIRST_NAME}                   Test
${LAST_NAME}                    User
${CONFIRM_PASSWORD}             TestPass123
${COMPANY_NAME}                 Test Company Ltd
${DATE_OF_BIRTH_DAY}            15
${DATE_OF_BIRTH_MONTH}          6
${DATE_OF_BIRTH_YEAR}           1990

# Product Search Data
${SEARCH_KEYWORD_ELECTRONICS}   laptop
${SEARCH_KEYWORD_APPAREL}       shirt
${SEARCH_KEYWORD_BOOKS}         programming
${SEARCH_KEYWORD_INVALID}       xyz123456789

# Contact Information
${CONTACT_FULL_NAME}            Test User
${CONTACT_EMAIL}                test@example.com
${CONTACT_SUBJECT}              Support
${CONTACT_ENQUIRY}              This is a test inquiry for automation testing purposes.

# Expected Messages
${LOGIN_SUCCESS_MESSAGE}        Welcome to our store
${REGISTRATION_SUCCESS}         Your registration completed
${CONTACT_SUCCESS}              Your enquiry has been successfully sent
${PRODUCT_NOT_FOUND}            No products were found that matched your criteria

# URLs
${HOME_URL}                     https://demo.nopcommerce.com/
${LOGIN_URL}                    https://demo.nopcommerce.com/login
${REGISTER_URL}                 https://demo.nopcommerce.com/register
${CONTACT_URL}                  https://demo.nopcommerce.com/contactus

# Browser Settings
${DEFAULT_TIMEOUT}              10
${LONG_TIMEOUT}                 30
${SHORT_TIMEOUT}                5

# Test Product Data
${TEST_PRODUCT_NAME}            Build your own computer
${TEST_PRODUCT_CATEGORY}        Computers
${TEST_PRODUCT_PRICE}           $1,200.00

# Edge Case Data
${EMPTY_STRING}                 ${EMPTY}
${SPACE_STRING}                 ${SPACE}
${SPECIAL_CHARS}                !@#$%^&*()
${VERY_LONG_STRING}             This is a very long string that exceeds normal input limits and should be used for testing maximum length validation scenarios in various input fields
${SQL_INJECTION}                ' OR '1'='1
${XSS_SCRIPT}                   <script>alert('XSS')</script>

# Mobile Test Data
${MOBILE_VIEWPORT_WIDTH}        375
${MOBILE_VIEWPORT_HEIGHT}       667
${TABLET_VIEWPORT_WIDTH}        768
${TABLET_VIEWPORT_HEIGHT}       1024

# API Test Data
${API_BASE_URL}                 https://api.example.com
${API_TIMEOUT}                  30
${API_HEADERS}                  Content-Type=application/json

# Dynamic Test Data
${RANDOM_STRING}                ${EMPTY}
${TIMESTAMP}                    ${EXECDIR}/../reports/timestamp.txt

# Test User Accounts
&{ADMIN_USER}
    ...    email=admin@demo.nopcommerce.com
    ...    password=admin
    ...    role=Administrator

&{REGULAR_USER}
    ...    email=test@example.com
    ...    password=TestPass123
    ...    role=Registered

&{GUEST_USER}
    ...    email=
    ...    password=
    ...    role=Guest

# Product Categories
@{CATEGORY_LIST}
    ...    Electronics
    ...    Apparel & Shoes
    ...    Digital downloads
    ...    Books
    ...    Jewelry
    ...    Gift Cards

# Payment Methods
@{PAYMENT_METHODS}
    ...    Credit Card
    ...    Purchase Order
    ...    Check / Money Order
    ...    PayPal
    ...    Cash On Delivery

# Shipping Methods
@{SHIPPING_METHODS}
    ...    Ground
    ...    Next Day Air
    ...    2nd Day Air

# Error Messages
${FIELD_REQUIRED_ERROR}         This is a required field.
${EMAIL_FORMAT_ERROR}           Wrong email
${PASSWORD_MISMATCH_ERROR}      The password and confirmation password do not match.
${LOGIN_FAILED_ERROR}           Login was unsuccessful. Please correct the errors and try again.
${PRODUCT_OUT_OF_STOCK}         The product is not available in the desired quantity.

# Success Messages
${ORDER_PLACED_SUCCESS}         Your order has been successfully processed!
${WISHLIST_ADDED_SUCCESS}        The product has been added to your wishlist
${COMPARE_ADDED_SUCCESS}         The product has been added to your compare list
${CART_UPDATED_SUCCESS}          The shopping cart has been updated

# Performance Test Data
${PERFORMANCE_TEST_ITERATIONS}    10
${PERFORMANCE_MAX_RESPONSE_TIME}  5000
${PERFORMANCE_MIN_THROUGHPUT}     100

# Visual Testing Data
${VISUAL_BASELINE_TOLERANCE}      0.95
${VISUAL_DIFFERENCE_THRESHOLD}    0.1
${SCREENSHOT_COMPRESSION_QUALITY}=    85

# Accessibility Test Data
${ACCESSIBILITY_WCAG_LEVEL}       AA
${ACCESSIBILITY_MIN_SCORE}        80
${ACCESSIBILITY_COLOR_CONTRAST}   4.5

# Security Test Data
${SECURITY_SQL_PAYLOADS}
    ...    ' OR '1'='1
    ...    ' OR '1'='2
    ...    admin'--
    ...    1' ORDER BY 1--
    ...    1' UNION SELECT 1,2,3--

${SECURITY_XSS_PAYLOADS}
    ...    <script>alert('XSS')</script>
    ...    <img src=x onerror=alert('XSS')>
    ...    javascript:alert('XSS')
    ...    <svg onload=alert('XSS')>
    ...    <iframe src=javascript:alert('XSS')>

${SECURITY_PATH_TRAVERSAL}
    ...    ../../../etc/passwd
    ...    ..\\..\\..\\windows\\system32\\config
    ...    /etc/shadow
    ...    C:\\Windows\\System32\\drivers\\etc\\hosts
