from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import asyncio
from . import playwright_pages
def get_social_media_links(url):

    driver = webdriver.Chrome()
    try:
        driver.get(url)
        social_media_links = []
        social_media_platforms = ["instagram.com","facebook.com", "twitter.com", "linkedin.com" ]

        for platform in social_media_platforms:
            elements = driver.find_elements(By.XPATH, f"//a[contains(@href, '{platform}')]")
            for element in elements:
                social_media_links.append(element.get_attribute("href"))
        if len(social_media_links) == 0:
            return "No social media links found"
        if len(social_media_links) == 1:
            asyncio.run(playwright_pages.run(social_media_links[0],"","","",))
        if len(social_media_links) == 2:
            asyncio.run(playwright_pages.run(social_media_links[0],social_media_links[1],"",""))
        if len(social_media_links) == 3:
            asyncio.run(playwright_pages.run(social_media_links[0],social_media_links[1],social_media_links[2],""))
        if len(social_media_links) == 4:
            asyncio.run(playwright_pages.run(social_media_links[0],social_media_links[1],social_media_links[2],social_media_links[3]))
        return social_media_links

    finally:

        driver.quit()

