from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def scrape_linkedin_posts(num_posts):
    options = Options()
    options.headless = True
    service = Service(r"S:\nayaone\chromium\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    posts = []

    driver.get('https://www.linkedin.com/pulse/topics/home/?trk=guest_homepage-basic_guest_nav_menu_articles')
    time.sleep(5)

    for idx in range(1, num_posts + 1):
        try:
            post = driver.find_elements(By.TAG_NAME, 'h2')[idx].text
            if post != '':
                posts.append(post)
            print(f"{idx} post(s) scraped...")
        except IndexError:
            print("All the posts from this page have been scraped!")
            break

    driver.quit()
    return posts