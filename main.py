import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class LoginAutomation:
    def __init__(self, headless=False):
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        
        if headless:
            self.options.add_argument("--headless")
        
        self.service = Service(ChromeDriverManager().install())
        self.driver = None
        
    def setup_driver(self):
        """Initialize the WebDriver"""
        try:
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
            return True
        except Exception as e:
            print(f"Failed to initialize WebDriver: {str(e)}")
            return False

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"Timeout waiting for element: {value}")
            return None

    def handle_captcha(self):
        """Handle reCAPTCHA if present"""
        try:
            # Wait for and switch to captcha iframe
            iframe = self.wait_for_element(
                By.XPATH, 
                "//iframe[@title='reCAPTCHA']",
                timeout=5
            )
            if not iframe:
                print("No CAPTCHA detected, continuing...")
                return True

            self.driver.switch_to.frame(iframe)
            
            # Find and click the captcha checkbox
            captcha_checkbox = self.wait_for_element(
                By.CSS_SELECTOR,
                ".recaptcha-checkbox-border"
            )
            if captcha_checkbox:
                self.driver.execute_script("arguments[0].click();", captcha_checkbox)
                time.sleep(2)  # Brief wait for animation
                self.driver.switch_to.default_content()
                return True
                
            return False
        except Exception as e:
            print(f"Error handling CAPTCHA: {str(e)}")
            self.driver.switch_to.default_content()
            return False

    def login(self, url, email, password):
        """Perform login operation"""
        try:
            print(f"\nAttempting login at: {url}")
            self.driver.get(url)

            # Find and fill email field
            email_field = self.wait_for_element(By.ID, "email")
            if not email_field:
                raise Exception("Email field not found")
            email_field.clear()
            email_field.send_keys(email)
            print("Email entered successfully")

            # Find and fill password field
            password_field = self.wait_for_element(By.ID, "password")
            if not password_field:
                raise Exception("Password field not found")
            password_field.clear()
            password_field.send_keys(password)
            print("Password entered successfully")

            # Handle CAPTCHA if present
            if not self.handle_captcha():
                print("CAPTCHA handling failed")
                return False

            # Click login button
            login_button = self.wait_for_element(By.ID, "submit")
            if not login_button:
                raise Exception("Login button not found")
            
            self.driver.execute_script("arguments[0].click();", login_button)
            print("Login button clicked")

            # Wait for login completion (adjust timeout as needed)
            # Add specific post-login element check here if possible
            time.sleep(5)
            
            # Add validation for successful login here
            # For example, check for a dashboard element or user profile
            # current_url = self.driver.current_url
            # if "dashboard" in current_url:
            #     print("Login successful!")
            # else:
            #     print("Login might have failed - please verify")
            
            return True

        except Exception as e:
            print(f"Login failed: {str(e)}")
            traceback.print_exc()
            return False

    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            print("Browser closed and resources cleaned up")

def main():
    # Configuration
    servers = [
        "https://app.certifyme.online/auth/login"
    ]
    email = "neeraj@certifyme.cc"
    password = "Neeraj@3235"

    # Initialize automation
    automation = LoginAutomation(headless=False)
    if not automation.setup_driver():
        print("Failed to initialize automation")
        return

    try:
        # Test login for each server
        for server in servers:
            success = automation.login(server, email, password)
            if success:
                print(f"Login test completed for {server}")
            else:
                print(f"Login test failed for {server}")
            
    except Exception as e:
        print("An unexpected error occurred:")
        traceback.print_exc()
    
    finally:
        automation.cleanup()
        print("Testing completed for all servers.")

if __name__ == "__main__":
    main()
