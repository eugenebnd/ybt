from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tempfile
import os

def simulate_view(video_id):
    try:
        options = webdriver.ChromeOptions()

        # Create a temporary directory for user data
        temp_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={temp_dir}")

        # Add other helpful options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--mute-audio")
        options.add_argument("--window-size=1920,1080")

        # Add language preference to get English consent dialog
        options.add_argument("--lang=en-US")

        driver = webdriver.Chrome(options=options)
        driver.get(f"https://www.youtube.com/watch?v={video_id}")

        # Take a screenshot before accepting cookies
        screenshot_path = f"screenshot_before_cookies_{video_id}.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {os.path.abspath(screenshot_path)}")

        # Wait for the page to load
        time.sleep(10)

        # Try multiple approaches to handle the cookie consent dialog
        try:
            # Method 1: Try to find the button by its text content (case insensitive)
            try:
                accept_buttons = driver.find_elements(By.XPATH,
                    "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept all') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'i agree')]")

                if accept_buttons:
                    for button in accept_buttons:
                        try:
                            print(f"Found button with text: {button.text}")
                            driver.execute_script("arguments[0].click();", button)
                            print("Clicked button using JavaScript")
                            time.sleep(2)
                            break
                        except Exception as e:
                            print(f"Failed to click button: {e}")
                else:
                    print("No buttons with accept/agree text found")
            except Exception as e:
                print(f"Method 1 failed: {e}")

        except Exception as e:
            print(f"Could not handle consent dialog: {e}")

        # Take a screenshot after attempting to handle cookies
        screenshot_path = f"screenshot_after_cookies_{video_id}.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {os.path.abspath(screenshot_path)}")

        # Use the updated method to find elements
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.SPACE)  # Play the video

        # Wait a bit and take another screenshot while playing
        time.sleep(10)
        screenshot_path = f"screenshot_during_{video_id}.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {os.path.abspath(screenshot_path)}")

        # Continue watching
        time.sleep(27)  # Complete the total 37 seconds of watching

        # Take a final screenshot
        screenshot_path = f"screenshot_after_{video_id}.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {os.path.abspath(screenshot_path)}")

        driver.quit()

    except WebDriverException as e:
        print(f"Error: {e}")
        print("Ensure that ChromeDriver is installed and the path is correct.")

def main():
    video_id = "sYd2VK1uy2s"
    simulate_view(video_id)

if __name__ == "__main__":
    main()
