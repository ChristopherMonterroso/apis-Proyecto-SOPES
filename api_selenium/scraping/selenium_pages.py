from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio

async def run(instagram_url:str, facebook_url:str, twitter_url:str, linkedin_url:str):
    tasks = []

    if instagram_url!="":
        tasks.append(asyncio.create_task(get_info_instagram(instagram_url)))
    if facebook_url!="":
        tasks.append(asyncio.create_task(get_info_facebook(facebook_url)))
    if twitter_url!="":
        tasks.append(asyncio.create_task(get_info_twitter(twitter_url)))
    if linkedin_url!="":
        tasks.append(asyncio.create_task(get_info_linkedin(linkedin_url)))

    await asyncio.gather(*tasks)


async def get_info_instagram(url):
    # Set up the Chrome browser
    options = webdriver.ChromeOptions()
    options.headless = False  # Set to True if you don't want to see the browser window
    browser = webdriver.Chrome(options=options)

    try:
        browser.get('https://www.instagram.com/accounts/login/')
        # Wait for the login elements to be present before interacting with them
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        # Find the username and password input fields and login button
        username_input = browser.find_element(By.NAME, "username")
        password_input = browser.find_element(By.NAME, "password")
        login_button = browser.find_element(By.XPATH, "//button[@type='submit']")

        username_input.send_keys("sistemasoperativos1")
        password_input.send_keys("Sopes123")

        login_button.click()
        browser.get(url)

        pagina = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/a/h2"))
        ).text
        informacion = WebDriverWait(browser,10).until(
          EC.presence_of_element_located((By.XPATH,"//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/h1"))
        ).text
        followers = WebDriverWait(browser,10).until(
          EC.presence_of_element_located((By.XPATH,"//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span"))
        ).text
        posts = WebDriverWait(browser,10).until(
          EC.presence_of_element_located((By.XPATH,"//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span"))
        ).text
        followed = WebDriverWait(browser,10).until(
          EC.presence_of_element_located((By.XPATH,"//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span"))
        ).text
        with open('selenium_data_found/instagram.txt', 'w', encoding='utf-8') as file:
                file.write("Instagram De: " + pagina + "\n")
                file.write("Informacion: " + informacion + "\n")
                file.write("Publicaciones: " + posts + "\n")
                file.write("Seguidores: " + followers+ "\n")
                file.write("Seguidos: " + followed + "\n")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the browser
        browser.quit()

async def get_info_facebook(url):
    options = webdriver.ChromeOptions()
    options.headless = False  # Set to True if you don't want to see the browser window
    browser = webdriver.Chrome( options=options)

    try:
        browser.get(url)

        # Wait for the elements to be present before interacting with them
        pagina = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/div/div/span/h1"))
        ).text

        seguidores = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[2]"))
        ).text

        likes = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[1]"))
        ).text

        informacion = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/span"))
        ).get_attribute('innerHTML')

        with open('selenium_data_found/facebook.txt', 'w', encoding='utf-8') as file:
            file.write("Facebook De: " + pagina + "\n")
            file.write("Informacion: " + informacion + "\n")
            file.write("likes: " + likes + "\n")
            file.write("Seguidores: " + seguidores + "\n")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        browser.quit()

async def get_info_twitter(url):
    # Set up the Chrome browser
    options = webdriver.ChromeOptions()
    options.headless = False  # Set to True if you don't want to see the browser window
    browser = webdriver.Chrome(options=options)

    try:
        browser.get('https://twitter.com/i/flow/login')
         # Wait for the login elements to be present before interacting with them
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'text')))
        # Find the username and password input fields and login button
        username_input = browser.find_element(By.NAME, 'text')
        username_input.send_keys("SistemasOp1")
        next_button = browser.find_element(By.XPATH, "//html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]")
        next_button.click()  
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
        password_input = browser.find_element(By.NAME, "password")
        password_input.send_keys("sistemasoperativos1")
        login_button = browser.find_element(By.XPATH, "//html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div")
        login_button.click()
        browser.get(url)
        WebDriverWait(browser,10)

        pagina = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span/span[1]"))
        ).text
        informacion = WebDriverWait(browser,10).until(
          EC.presence_of_element_located((By.XPATH,"//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[3]/div/div[1]/span"))
        ).text
        followers = WebDriverWait(browser,10).until(
          EC.presence_of_element_located((By.XPATH,"//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span"))
        ).text

        followed = WebDriverWait(browser,10).until(
          EC.presence_of_element_located((By.XPATH,"//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span"))
        ).text
        with open('selenium_data_found/twitter.txt', 'w', encoding='utf-8') as file:
                file.write("Twitter De: " + pagina + "\n")
                file.write("Informacion: " + informacion + "\n")
                file.write("Seguidores: " + followers+ "\n")
                file.write("Seguidos: " + followed + "\n")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the browser
        browser.quit()

async def get_info_linkedin(url):
    options = webdriver.ChromeOptions()
    options.headless = False  # Set to True if you don't want to see the browser window
    browser = webdriver.Chrome( options=options)

    try:
        browser.get(url)

        # Wait for the elements to be present before interacting with them
        pagina = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/main/section[1]/section/div/div[2]/div[1]/h1"))
        ).text

        informacion = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/main/section[1]/section/div/div[2]/div[1]/h2"))
        ).text

        tamano = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/main/section[1]/div/section[1]/div/dl/div[3]/dd"))
        ).text

        seguidores = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/main/section[1]/section/div/div[2]/div[1]/h3"))
        ).text

        with open('selenium_data_found/linkedin.txt', 'w', encoding='utf-8') as file:
            file.write("Linkedin De: " + pagina + "\n")
            file.write("Informacion: " + informacion + "\n")
            file.write("tamano: " + tamano + "\n")
            file.write("Seguidores: " + seguidores + "\n")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        browser.quit()

if __name__ == "__main__":
    asyncio.run(run('https://www.instagram.com/eltallerdetephy.gt/','','',''))