from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def simulate_view(video_id):
    driver = webdriver.Chrome()
    driver.get(f"https://www.youtube.com/watch?v={video_id}")
    time.sleep(5)  # Wait for the video to load
    driver.find_element_by_tag_name('body').send_keys(Keys.SPACE)  # Play the video
    time.sleep(10)  # Watch the video for 10 seconds
    driver.quit()

def main():
    video_id = input("Enter the video ID to simulate a view: ")
    simulate_view(video_id)

if __name__ == "__main__":
    main()
