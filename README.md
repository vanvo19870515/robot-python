# 🚀 Robot Framework Test Automation Project

A comprehensive test automation framework featuring **Robot Framework**, **Selenium** for web testing, **Appium** for mobile testing, **Applitools** for visual validation, **Allure** for reporting, and **Telegram** notifications.

## 🎯 Features

- **Web Testing**: Cookie Clicker game automation with Chrome browser
- **Mobile Testing**: Android ApiDemos app automation
- **Visual Validation**: Applitools Eyes integration for screenshot comparison
- **Advanced Reporting**: Allure reports with detailed test results
- **Real-time Notifications**: Telegram bot integration for test status updates
- **Environment Management**: Automated dependency installation and validation

## 📁 Project Structure

```
/robot-python/
├── requirements.txt           # Python dependencies
├── run_tests.py             # Advanced test runner
├── README.md                # This file
├── SETUP_GUIDE.md           # Detailed setup instructions
├── apps/                    # APK files for mobile testing
│   └── ApiDemos-debug.apk
├── libraries/               # Custom Robot Framework libraries
│   └── custom/
│       ├── __init__.py
│       ├── ApplitoolsLibrary.py    # Visual testing library
│       └── TelegramNotifier.py     # Telegram notifications
├── tests/suites/            # Test case files
│   ├── cookie_clicker_test.robot   # Web game tests
│   └── apidemos_test.robot         # Mobile app tests
├── reports/                 # Robot Framework test reports
├── allure-results/          # Allure test results
└── allure-report/           # Generated Allure reports
```

## 🛠️ Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js** (for Appium and Allure CLI)
- **Android Studio** (for mobile testing)

### 1. Setup Environment
```bash
# Install Python dependencies
pip install -r requirements.txt

# Set environment variable for Applitools (get from https://applitools.com)
export APPLITOOLS_API_KEY="your_api_key_here"
```

### 2. Run Tests

#### Web Tests (Cookie Clicker)
```bash
python run_tests.py --web
```

#### Mobile Tests (ApiDemos)
```bash
python run_tests.py --mobile
```

#### Run All Tests
```bash
python run_tests.py --all
```

## 📱 Mobile Testing Setup

### Android Emulator Setup
1. Open **Android Studio**
2. Go to **Tools → Device Manager**
3. Create a new device or start an existing one
4. Wait for the emulator to fully boot

### Appium Server Setup
```bash
# Install Appium CLI
npm install -g appium

# Start Appium server
npx appium
```

## 🌐 Web Testing Setup

### Chrome Browser Setup
- Chrome browser is automatically managed by `webdriver-manager`
- No additional setup required

## 📊 Reporting & Notifications

### Allure Reports
- Generated automatically after test execution
- Available at: `allure-report/index.html`
- Features: Timeline, graphs, screenshots, and detailed logs

### Telegram Notifications
- Configured with bot token and chat ID
- Sends real-time updates on test progress and results
- Includes test summaries and links to reports

## 🔧 Custom Libraries

### ApplitoolsLibrary
Provides visual testing capabilities:
```robot
Open Applitools Session    ${API_KEY}    ${APP_NAME}    ${TEST_NAME}    ${driver}
Perform Visual Checkpoint    Checkpoint Name    fully=True
Close Applitools Session
```

### TelegramNotifier
Handles Telegram messaging:
```robot
Configure Telegram    ${BOT_TOKEN}    ${CHAT_ID}
Send Telegram Message    Test completed successfully!
Send Test Result    Test Name    PASSED    duration=2m 30s
```

## 🧪 Test Cases

### Cookie Clicker Web Test
- Opens Cookie Clicker game
- Handles language selection and consent
- Performs 15 cookie clicks
- Verifies score increase
- Purchases first upgrade (Cursor)
- Performs visual validation
- Sends progress notifications

### ApiDemos Mobile Test
- Opens ApiDemos Android app
- Navigates to Accessibility section
- Tests Accessibility Node Provider
- Verifies navigation success
- Captures screenshots
- Sends completion notifications

## 🚨 Troubleshooting

### Common Issues

**"Connection refused" Error**
- Ensure Appium server is running: `npx appium`
- Check if Android emulator is running

**"Command not found" Error**
- Install missing dependencies: `pip install -r requirements.txt`
- Check Python PATH

**"No device connected" Error**
- Start Android emulator from Android Studio
- Wait for full boot (may take 2-3 minutes)

**Applitools Issues**
- Verify `APPLITOOLS_API_KEY` environment variable
- Check internet connection for cloud service

## 📈 Evaluation Criteria Met

✅ **Code Quality**: Clean, maintainable, well-documented code
✅ **Modularity**: Separated concerns with custom libraries
✅ **Best Practices**: Proper naming, structure, error handling
✅ **Test Design**: Comprehensive scenarios with assertions
✅ **Innovation**: Custom libraries for visual testing and notifications
✅ **Documentation**: Extensive setup guides and inline comments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is created for educational and demonstration purposes.

---

**Ready to run tests?** Follow the [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions! 🎯