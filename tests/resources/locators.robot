*** Variables ***
# Common Locators for nopCommerce Demo Site

# Home Page
${HOME_LOGO}                    //img[@alt='nopCommerce demo store']
${SEARCH_BOX}                   //input[@id='small-searchterms']
${SEARCH_BUTTON}                //button[contains(text(),'Search')]
${SHOPPING_CART}                //span[@class='cart-label']

# Login Page
${LOGIN_EMAIL}                  //input[@id='Email']
${LOGIN_PASSWORD}               //input[@id='Password']
${LOGIN_BUTTON}                 //button[contains(text(),'Log in')]
${LOGOUT_LINK}                  //a[contains(text(),'Log out')]

# Registration Page
${REG_GENDER_MALE}              //input[@id='gender-male']
${REG_GENDER_FEMALE}            //input[@id='gender-female']
${REG_FIRST_NAME}               //input[@id='FirstName']
${REG_LAST_NAME}                //input[@id='LastName']
${REG_EMAIL}                    //input[@id='Email']
${REG_PASSWORD}                 //input[@id='Password']
${REG_CONFIRM_PASSWORD}         //input[@id='ConfirmPassword']
${REG_REGISTER_BUTTON}          //button[@id='register-button']
${REG_SUCCESS_MESSAGE}          //div[@class='result']

# Product Page
${PRODUCT_GRID}                 //div[@class='product-grid']
${PRODUCT_ITEM}                 //div[@class='product-item']
${ADD_TO_CART_BUTTON}           //button[contains(text(),'Add to cart')]
${PRODUCT_NAME}                 //div[@class='product-name']//h1
${PRODUCT_PRICE}                //div[@class='product-price']//span

# Shopping Cart
${CART_TABLE}                   //div[@class='table-wrapper']
${CART_ITEM_ROW}                //tr[@class='cart-item-row']
${CART_QUANTITY_INPUT}          //input[@class='qty-input']
${GO_TO_CART_BUTTON}            //button[contains(text(),'Go to cart')]
${UPDATE_CART_BUTTON}           //button[@name='updatecart']
${REMOVE_FROM_CART}             //button[@class='remove-btn']

# Contact Us Page
${CONTACT_FULL_NAME}            //input[@id='FullName']
${CONTACT_EMAIL}                //input[@id='Email']
${CONTACT_ENQUIRY_DROPDOWN}     //select[@name='Enquiry']
${CONTACT_ENQUIRY_TEXT}         //textarea[@id='Enquiry']
${CONTACT_SUBMIT_BUTTON}        //button[contains(text(),'Submit')]

# Navigation
${NAVIGATION_MENU}              //div[@class='header-menu']
${CATEGORY_ELECTRONICS}         //a[contains(text(),'Electronics')]
${CATEGORY_APPAREL}             //a[contains(text(),'Apparel & Shoes')]
${CATEGORY_DIGITAL_DOWNLOADS}   //a[contains(text(),'Digital downloads')]

# Footer
${FOOTER_INFORMATION}           //div[@class='footer-block information']
${FOOTER_CUSTOMER_SERVICE}      //div[@class='footer-block customer-service']
${FOOTER_MY_ACCOUNT}            //div[@class='footer-block my-account']
${FOOTER_FOLLOW_US}             //div[@class='footer-block follow-us']

# User Account
${MY_ACCOUNT_LINK}              //a[contains(text(),'My account')]
${ADDRESSES_LINK}               //a[contains(text(),'Addresses')]
${ORDERS_LINK}                  //a[contains(text(),'Orders')]
${DOWNLOADABLE_PRODUCTS}        //a[contains(text(),'Downloadable products')]

# Wishlist
${WISHLIST_LINK}                //a[contains(text(),'Wishlist')]
${ADD_TO_WISHLIST}              //button[contains(text(),'Add to wishlist')]
${WISHLIST_TABLE}               //table[@class='wishlist-table']

# Compare Products
${COMPARE_LIST}                 //a[contains(text(),'Compare products list')]
${ADD_TO_COMPARE}               //button[contains(text(),'Add to compare')]
${COMPARE_TABLE}                //table[@class='compare-products-table']

# Newsletter
${NEWSLETTER_EMAIL}             //input[@id='newsletter-email']
${NEWSLETTER_SUBSCRIBE_BUTTON}  //button[@id='newsletter-subscribe-button']
${NEWSLETTER_UNSUBSCRIBE}       //a[contains(text(),'Unsubscribe')]

# Recently Viewed Products
${RECENTLY_VIEWED}              //div[@class='product-grid'][contains(.,'Recently viewed')]
${CLEAR_RECENTLY_VIEWED}        //a[contains(text(),'Clear')]

# Breadcrumb
${BREADCRUMB_HOME}              //div[@class='breadcrumb']//a[contains(text(),'Home')]
${BREADCRUMB_CURRENT}           //div[@class='breadcrumb']//strong

# Search Results
${SEARCH_RESULTS_TITLE}         //div[@class='page-title']//h1
${NO_RESULTS_MESSAGE}           //div[@class='no-result']
${SEARCH_TERM_LABEL}            //span[@class='search-term']

# Error Messages
${ERROR_MESSAGE}                //div[@class='message-error']
${VALIDATION_ERROR}             //span[@class='field-validation-error']
${SUCCESS_MESSAGE}              //div[@class='message-success']

# Loading Indicators
${LOADING_OVERLAY}              //div[@class='loading-overlay']
${AJAX_LOADING}                 //div[@class='ajax-loading-block-window']

# Mobile Specific
${MOBILE_MENU_TOGGLE}           //button[@class='mobile-menu-toggle']
${MOBILE_NAVIGATION}            //div[@class='mobile-navigation']

# Accessibility
${SKIP_TO_CONTENT}              //a[@class='skip-link']
${ARIA_LIVE_REGION}             //div[@aria-live='polite']

# Common UI Elements
${HEADER_LOGO}                  //div[@class='header-logo']//a//img
${HEADER_LINKS}                 //div[@class='header-links']
${FOOTER}                       //div[@class='footer']
${CONTENT}                      //div[@class='master-wrapper-content']
${SIDE_BAR}                     //div[@class='side-bar']
${MAIN_CONTENT}                 //div[@class='main-content']

# Dynamic Locators (use with caution)
${DYNAMIC_BUTTON_BY_TEXT}       //button[contains(text(),'{0}')]
${DYNAMIC_LINK_BY_TEXT}         //a[contains(text(),'{0}')]
${DYNAMIC_INPUT_BY_ID}          //input[@id='{0}']
${DYNAMIC_DIV_BY_CLASS}         //div[@class='{0}']
${DYNAMIC_SPAN_BY_TEXT}         //span[contains(text(),'{0}')]
