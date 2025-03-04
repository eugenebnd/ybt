from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
import time
import tempfile
import os
import random
import requests
from fake_useragent import UserAgent

def get_random_proxy():
    # Replace with your proxy service or list of proxies
    proxies = [
        "http://102.0.17.224:8080/",
        # Add more proxies as needed
    ]
    return random.choice(proxies)

def random_sleep(min_time=1, max_time=5):
    time.sleep(random.uniform(min_time, max_time))

def simulate_human_scroll(driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    current_position = 0
    while current_position < total_height:
        # Random scroll amount
        scroll_amount = random.randint(100, 300)
        current_position += scroll_amount

        # Scroll with a random speed
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        random_sleep(0.5, 2)

        # Sometimes pause longer as if reading content
        if random.random() < 0.2:
            random_sleep(2, 5)

def simulate_view(video_id):
    try:
        # Create a user agent
        ua = UserAgent()
        user_agent = ua.random

        options = webdriver.ChromeOptions()

        # Create a temporary directory for user data
        temp_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={temp_dir}")

        # Set a random user agent
        options.add_argument(f'user-agent={user_agent}')

        # Add other helpful options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--mute-audio")

        # Remove headless mode to appear more like a real user
        # options.add_argument("--headless")

        # Set window size to a common resolution
        window_width = random.choice([3840])
        window_height = random.choice([2160])
        options.add_argument(f"--window-size={window_width},{window_height}")

        # Add language preference with some randomization
        languages = ["en-US", "en-GB", "en-CA", "en-AU"]
        options.add_argument(f"--lang={random.choice(languages)}")

        # Disable automation flags
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Optional: Add proxy support
        proxy = get_random_proxy()
        options.add_argument(f'--proxy-server={proxy}')

        driver = webdriver.Chrome(options=options)

        # Apply stealth settings to make selenium undetectable
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        # Set additional headers to appear more like a browser
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": user_agent,
            "acceptLanguage": "en-US,en;q=0.9"
        })

        # Set cookies before visiting the site
        driver.get("https://www.youtube.com")
        random_sleep(2, 4)

        # Take a screenshot before accepting cookies
        screenshot_path = f"screenshot_before_cookies_{video_id}.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {os.path.abspath(screenshot_path)}")

        # Navigate to the video with some randomness in timing
        print(f"Navigating to video: {video_id}")
        driver.get(f"https://www.youtube.com/watch?v={video_id}")
        random_sleep(3, 7)

        # Handle cookie consent dialog with more human-like interaction
        try:
            accept_buttons = driver.find_elements(By.XPATH,
                "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept all') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'i agree')]")

            if accept_buttons:
                # Choose a random button if multiple are found
                button = random.choice(accept_buttons)
                print(f"Found consent button with text: {button.text}")

                # Move mouse to button before clicking (more human-like)
                actions = ActionChains(driver)
                actions.move_to_element(button).pause(random.uniform(0.5, 1.5)).click().perform()
                print("Clicked consent button")
                random_sleep(1, 3)
            else:
                print("No consent buttons found, may have been accepted already")
        except Exception as e:
            print(f"Handling consent dialog: {e}")

        # Simulate some scrolling before playing
        simulate_human_scroll(driver)

        screenshot_path = f"screenshot_scroll_{video_id}.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {os.path.abspath(screenshot_path)}")

        # Interact with video player in a more human-like way
        try:
            # Sometimes click on the video to play instead of using keyboard
            if random.random() < 0.7:
                video_player = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "movie_player"))
                )

                # Move to a random position within the player before clicking
                player_rect = video_player.rect
                x_offset = random.randint(int(player_rect['width']*0.3), int(player_rect['width']*0.7))
                y_offset = random.randint(int(player_rect['height']*0.3), int(player_rect['height']*0.7))

                actions = ActionChains(driver)
                actions.move_to_element_with_offset(video_player, x_offset, y_offset).pause(0.5).click().perform()
                print("Clicked on video player")
            else:
                # Use keyboard shortcut occasionally
                body = driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.SPACE)
                print("Used space key to play video")
        except Exception as e:
            print(f"Error interacting with video player: {e}")
            # Fallback to keyboard
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.SPACE)

        # Simulate watching with random interactions
        total_watch_time = random.randint(35, 120)  # Watch between 35-120 seconds
        elapsed_time = 0

        print(f"Planning to watch for {total_watch_time} seconds")

        while elapsed_time < total_watch_time:
            # Determine how long to watch before next interaction
            watch_segment = random.randint(5, 20)
            if elapsed_time + watch_segment > total_watch_time:
                watch_segment = total_watch_time - elapsed_time

            random_sleep(watch_segment, watch_segment + 1)
            elapsed_time += watch_segment

            # Randomly perform different interactions
            interaction = random.random()

            if interaction < 0.2 and elapsed_time < total_watch_time * 0.8:
                # Pause and resume (20% chance, only in first 80% of video)
                body = driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.SPACE)
                print("Paused video")
                random_sleep(1, 4)
                body.send_keys(Keys.SPACE)
                print("Resumed video")
            elif interaction < 0.4:
                # Adjust volume (20% chance)
                for _ in range(random.randint(1, 3)):
                    if random.random() < 0.5:
                        body = driver.find_element(By.TAG_NAME, 'body')
                        body.send_keys(Keys.ARROW_UP)  # Volume up
                    else:
                        body = driver.find_element(By.TAG_NAME, 'body')
                        body.send_keys(Keys.ARROW_DOWN)  # Volume down
                    random_sleep(0.3, 0.7)
                print("Adjusted volume")
            elif interaction < 0.5:
                # Scroll to comments section (10% chance)
                simulate_human_scroll(driver)
                print("Scrolled through page")
                random_sleep(2, 5)
                # Scroll back up to video
                driver.execute_script("window.scrollTo(0, 0);")
                random_sleep(1, 2)

            print(f"Watched for {elapsed_time} seconds so far")

        print(f"Finished watching video for {elapsed_time} seconds")
        random_sleep(2, 5)

        driver.quit()
        print("Browser closed successfully")
        return True

    except WebDriverException as e:
        print(f"WebDriver Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

    return False

def main():
    video_id = "sYd2VK1uy2s"
    success = False

    # Try up to 3 times with different settings if needed
    for attempt in range(3):
        if attempt > 0:
            print(f"Retry attempt {attempt}")
            time.sleep(random.randint(30, 60))  # Wait between attempts

        success = simulate_view(video_id)
        if success:
            break

if __name__ == "__main__":
    main()
