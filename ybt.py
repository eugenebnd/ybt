from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time

def simulate_view(video_id):
    try:
        options = webdriver.ChromeOptions()
        # Add some options to make it more stable
        options.add_argument("--mute-audio")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")

        # Create the driver with service object
        driver = webdriver.Chrome(options=options)
        driver.get(f"https://www.youtube.com/watch?v={video_id}")

        print("Loading video...")
        time.sleep(5)  # Wait for the video to load

        # Use the updated method to find elements with By
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.SPACE)  # Play the video

        print("Watching video for 10 seconds...")
        time.sleep(10)  # Watch the video for 10 seconds

        print("Done watching. Closing browser.")
        driver.quit()

    except WebDriverException as e:
        print(f"Error: {e}")
        print("Ensure that ChromeDriver is installed and the path is correct.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    video_id = input("Enter the video ID to simulate a view: ")
    simulate_view(video_id)

if __name__ == "__main__":
    main()
