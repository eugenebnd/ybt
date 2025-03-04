from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import tempfile

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

        driver = webdriver.Chrome(options=options)
        driver.get(f"https://www.youtube.com/watch?v={video_id}")
        time.sleep(5)  # Wait for the video to load

        # Use the updated method to find elements
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.SPACE)  # Play the video

        time.sleep(37)  # Watch the video for 10 seconds
        driver.quit()

    except WebDriverException as e:
        print(f"Error: {e}")
        print("Ensure that ChromeDriver is installed and the path is correct.")

def main():
    video_id = "DxI8qY_N-N4"
    simulate_view(video_id)

if __name__ == "__main__":
    main()
