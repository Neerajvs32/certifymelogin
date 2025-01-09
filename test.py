import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up WebDriver
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# List of servers to test
servers = [
    "https://app.certifyme.online/auth/login"
]

try:
    for server in servers:
        print(f"Testing login for server: {server}")
        driver.get(server)

        # Locate username and password fields
        try:
            print("Attempting to locate username field...")
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            print("Username field located. Entering credentials...")
            username_field.send_keys("neeraj@certifyme.cc")

            password_field = driver.find_element(By.ID, "password")
            print("Password field located. Entering credentials...")
            password_field.send_keys("Neeraj@3235")
        except Exception as field_error:
            print("Error locating username or password fields:", field_error)
            continue

        # Handle CAPTCHA
        try:
            print("Checking for CAPTCHA iframe...")
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']"))
            )
            print("CAPTCHA iframe located. Attempting to click checkbox...")
            captcha_checkbox = driver.find_element(By.CSS_SELECTOR, ".recaptcha-checkbox-border")
            driver.execute_script("arguments[0].click();", captcha_checkbox)
            print("CAPTCHA checkbox clicked.")
            time.sleep(10)  # Allow time for CAPTCHA to process (adjust as needed)
            driver.switch_to.default_content()
        except Exception as captcha_error:
            print("CAPTCHA handling failed:", captcha_error)
            continue

        # Submit the login form
        try:
            print("Attempting to click login button...")
            login_button = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].click();", login_button)  # Use JS to avoid interception issues
            print("Login button clicked. Waiting for login to complete...")
            time.sleep(15)  # Adjust time based on server response speed

            # Check for successful login (add a specific post-login element check if needed)
            print(f"Login test for {server} completed.")
        except Exception as login_error:
            print("Error during login:", login_error)

except Exception as e:
    print("An unexpected error occurred:")
    traceback.print_exc()

finally:
    # Quit the browser
    driver.quit()
    print("Testing completed for all servers.")
