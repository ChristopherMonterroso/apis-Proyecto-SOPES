from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from . import selenium_pages
import asyncio
def get_social_media_links(url):
    print("hizo esto")
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    print("hizo esto2")
    driver = webdriver.Chrome(options=chrome_options)

    print("viene aqui")
    try:
        driver.get(url)
        
        social_media_links = []
        social_media_platforms = ["instagram.com","facebook.com", "twitter.com", "linkedin.com" ]

        for platform in social_media_platforms:
            elements = driver.find_elements(By.XPATH, f"//a[contains(@href, '{platform}')]")
            for element in elements:
                social_media_links.append(element.get_attribute("href"))
        print("vamos bien")
        if len(social_media_links) == 0:
            return "No social media links found"
        if len(social_media_links) == 1:
            asyncio.run(selenium_pages.run(social_media_links[0],"","","",))
        if len(social_media_links) == 2:
            asyncio.run(selenium_pages.run(social_media_links[0],social_media_links[1],"",""))
        if len(social_media_links) == 3:
            asyncio.run(selenium_pages.run(social_media_links[0],social_media_links[1],social_media_links[2],""))
        if len(social_media_links) == 4:
            asyncio.run(selenium_pages.run(social_media_links[0],social_media_links[1],social_media_links[2],social_media_links[3]))
        
        print(social_media_links)
        return social_media_links
    finally:
        driver.quit()
