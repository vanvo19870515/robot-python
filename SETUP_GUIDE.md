# 🚀 Complete Setup Guide for Test Automation Project

This guide provides step-by-step instructions to set up and run the comprehensive test automation framework.

## 📋 Prerequisites Checklist

- [ ] **Python 3.8+** installed
- [ ] **Node.js** installed (for Appium and Allure)
- [ ] **Android Studio** installed (for mobile testing)
- [ ] **Git** (optional, for version control)

## 🛠️ Step 1: Environment Setup

### 1.1 Install Python Dependencies
```bash
# Navigate to project directory
cd /path/to/robot-python

# Install all required Python packages
pip install -r requirements.txt
```

**Expected Output:**
```
✅ Robot Framework is installed
✅ Dependencies installed successfully
```

### 1.2 Set Environment Variables

**For Applitools Visual Testing:**
```bash
# Get your API key from https://applitools.com
export APPLITOOLS_API_KEY="your_api_key_here"
```

**For Telegram Notifications:**
The bot credentials are already configured in the code:
- Bot Token: `8387676250:AAH1VNxOofEKA04ilK90zPA0zoZ1tFjXuzk`
- Chat ID: `6225001877`

## 📱 Step 2: Mobile Testing Setup (Android)

### 2.1 Install Android Studio
1. Download from: https://developer.android.com/studio
2. Install following the setup wizard
3. **Important**: Choose "Custom" installation and ensure "Android SDK" is selected

### 2.2 Configure Android SDK
1. Open **Android Studio**
2. Go to **Tools → SDK Manager**
3. In **SDK Platforms** tab:
   - Select **Android 13.0 (Tiramisu)** or latest version
   - Click **Apply** to download
4. In **SDK Tools** tab:
   - Ensure **Android SDK Build-Tools**, **Android SDK Platform-Tools**, and **Android Emulator** are installed
   - Click **Apply** if needed

### 2.3 Create Android Emulator
1. In Android Studio, go to **Tools → Device Manager**
2. Click **"Create device"**
3. Choose **Phone → Pixel 6** (or similar)
4. Select **Android 13.0** system image
5. Click **"Next"** and **"Finish"**

### 2.4 Start Emulator
1. In Device Manager, find your created device
2. Click the **Play button (▶️)**
3. Wait 2-3 minutes for full boot (you'll see Android home screen)

## 🌐 Step 3: Appium Setup

### 3.1 Install Appium
```bash
# Install Appium globally
npm install -g appium

# Install UiAutomator2 driver for Android
npx appium driver install uiautomator2
```

### 3.2 Start Appium Server
```bash
# Terminal 1 - Start server
npx appium
```

**Expected Output:**
```
[Appium] Appium REST http interface listener started on http://0.0.0.0:4723
```

**Keep this terminal window open!**

## 🧪 Step 4: Run Tests

### 4.1 Web Test (Cookie Clicker)
```bash
# Terminal 2 - Run web tests
python run_tests.py --web
```

**What it does:**
- Opens Cookie Clicker game in Chrome
- Handles language selection and consent
- Clicks cookie 15 times
- Verifies score increase
- Buys first upgrade (Cursor)
- Performs visual validation with Applitools
- Sends Telegram notifications

### 4.2 Mobile Test (ApiDemos)
```bash
# Terminal 2 - Run mobile tests
python run_tests.py --mobile
```

**What it does:**
- Installs and opens ApiDemos app on Android emulator
- Navigates to Accessibility → Node Provider
- Verifies navigation success
- Captures screenshots
- Sends Telegram notifications

### 4.3 Run All Tests
```bash
python run_tests.py --all
```

## 📊 Step 5: View Reports

### Allure Reports
- **Location**: `allure-report/index.html`
- **Features**: Timeline, graphs, screenshots, detailed logs
- **Open**: Double-click `index.html` or open in browser

### Telegram Notifications
- Real-time updates sent to configured chat
- Includes test progress and final results
- Links to Allure reports

## 🔍 Step 6: Troubleshooting

### Common Issues & Solutions

**❌ "Connection refused"**
- **Cause**: Appium server not running
- **Solution**: Ensure `npx appium` is running in Terminal 1

**❌ "Could not find a connected Android device"**
- **Cause**: Android emulator not started
- **Solution**: Start emulator from Android Studio Device Manager

**❌ "Command not found: appium"**
- **Cause**: Appium not installed or PATH not set
- **Solution**: Run `npm install -g appium`

**❌ "No module named 'robot'"**
- **Cause**: Dependencies not installed
- **Solution**: Run `pip install -r requirements.txt`

**❌ Applitools visual validation fails**
- **Cause**: Invalid API key or network issues
- **Solution**: Check `APPLITOOLS_API_KEY` and internet connection

**⚠️ Telegram notifications not working**
- **Cause**: Bot token or chat ID issues
- **Solution**: Verify credentials in `TelegramNotifier.py`

### Debug Commands
```bash
# Check Android devices
adb devices

# Check Appium status
curl http://localhost:4723/wd/hub/status

# Check environment variables
echo $APPLITOOLS_API_KEY

# Check Python imports
python -c "import robot; print('Robot OK')"
```

## 🎯 Step 7: Verification

After successful setup, you should see:

**Terminal Output:**
```
🔧 Setting up test environment...
✅ Robot Framework is installed
🍪 Running Cookie Clicker Tests...
✅ Cookie Clicker tests completed successfully
🎨 Generating Allure report...
✅ Allure report generated successfully
📊 Report available at: /path/to/allure-report/index.html
✅ Telegram notification sent successfully
🎉 Test execution completed successfully!
```

**Allure Report:**
- Beautiful HTML report with test details
- Screenshots and step-by-step logs
- Timeline and analytics

**Telegram Messages:**
- Real-time test progress updates
- Final summary with success/failure status
- Links to detailed reports

## 🚀 Next Steps

1. **Explore Test Results**: Open `allure-report/index.html`
2. **Customize Tests**: Modify test cases in `tests/suites/`
3. **Add More Tests**: Create additional test scenarios
4. **CI/CD Integration**: Set up automated test execution

## 💬 Support

If you encounter issues:
1. Check this setup guide
2. Review troubleshooting section
3. Check the detailed logs in `reports/`
4. Verify all prerequisites are installed

---

**🎉 Congratulations!** Your comprehensive test automation framework is now ready for production use! 🚀