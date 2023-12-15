import asyncio
from playwright.async_api import async_playwright

async def run(instagram_url,facebook_url,  twitter_url, linkedin_url):
    tasks = []

    if facebook_url!="":
        tasks.append(asyncio.create_task(get_info_facebook(facebook_url)))
    if instagram_url!="":
        tasks.append(asyncio.create_task(get_info_instagram(instagram_url)))
    if twitter_url!="":
        tasks.append(asyncio.create_task(get_info_twitter(twitter_url)))
    if linkedin_url!="":
        tasks.append(asyncio.create_task(get_info_linkedin(linkedin_url)))

    await asyncio.gather(*tasks)


    
async def get_info_instagram(url):
    
    with async_playwright() as p:
        browser =  p.chrome.launch(headless=False, slow_mo=50,args=['--no-sandbox', '--disable-gpu', '--disable-software-rasterizer'])
        page =  browser.new_page()
        try:
            page.goto('https://www.instagram.com/accounts/login/')
            page.fill('input[name="username"]', 'sistemasoperativos1')
            page.fill('input[name="password"]', 'Sopes123')
            page.click('button[type="submit"]')
            page.wait_for_timeout(5000)
            page.goto(url)
            page.wait_for_timeout(5000)
            pagina =  page.locator("//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/a/h2").inner_text()
            informacion =  page.locator("//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/h1").inner_text()
            seguidores =  page.locator("//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span").inner_text()
            publicaciones =  page.locator("//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span").inner_text()
            seguidos =  page.locator("//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span").inner_text()
            with open('instagram.txt', 'w', encoding='utf-8') as file:
                file.write("Instagram De: " + pagina + "\n")
                file.write("Informacion: " + informacion + "\n")
                file.write("Publicaciones: " + publicaciones + "\n")
                file.write("Seguidores: " + seguidores + "\n")
                file.write("Seguidos: " + seguidos + "\n")
        except Exception as e:
            print(f"Error: {e}")
        finally:
             browser.close()

async def get_info_facebook(url):
    with async_playwright() as p:
        browser = p.chrome.launch(headless=False, slow_mo=50,args=['--no-sandbox', '--disable-gpu', '--disable-software-rasterizer'])
        page =  browser.new_page()
        try:
           page.goto(url)
           pagina = page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/div/div/span/h1").inner_text()                  
           seguidores = page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[2]").inner_text()
           likes = page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[1]").inner_text()
           informacion =  page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/span").inner_html()         
           with open('facebook.txt', 'w', encoding='utf-8') as file:
                file.write("Facebook De: " + pagina + "\n")
                file.write("Informacion: " + informacion + "\n")
                file.write("likes: " + likes + "\n")
                file.write("Seguidores: " + seguidores + "\n")
        except Exception as e:
            print(f"Error: {e}")
        finally:
             browser.close()

async def get_info_twitter(url):
      with async_playwright() as p:
        browser =  p.chrome.launch(headless=False, slow_mo=50,args=['--no-sandbox', '--disable-gpu', '--disable-software-rasterizer'])
        page =  browser.new_page()
        try:
            page.goto('https://twitter.com/i/flow/login')
            page.fill('input[name="text"]', 'SistemasOp1')
            page.locator("//html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]").click()
            page.fill('input[name="password"]', 'sistemasoperativos1')
            page.locator("//html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div").click()
            page.goto(url)
            pagina =  page.locator("//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span/span[1]").inner_text()
            informacion =  page.locator("//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[3]/div/div[1]/span").inner_text()
            seguidores =  page.locator("//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span").inner_text()
            seguidos =  page.locator("//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span").inner_text()
            with open('twitter.txt', 'w', encoding='utf-8') as file:
                  file.write("Twiter De: " + pagina + "\n")
                  file.write("Informacion: " + informacion + "\n")
                  file.write("Seguidores: " + seguidores + "\n")
                  file.write("Seguidos: " + seguidos + "\n")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
    
async def get_info_linkedin(url):
     with async_playwright() as p:
        browser = p.chrome.launch(headless=False, slow_mo=50,args=['--no-sandbox', '--disable-gpu', '--disable-software-rasterizer'])
        page =  browser.new_page()
        try:
            page.goto(url)
            pagina =  page.locator("//html/body/main/section[1]/section/div/div[2]/div[1]/h1").inner_text()
            informacion = page.locator("//html/body/main/section[1]/section/div/div[2]/div[1]/h2").inner_text()
            tamaño =  page.locator("//html/body/main/section[1]/div/section[1]/div/dl/div[3]/dd").inner_text()
            seguidores=  page.locator("//html/body/main/section[1]/section/div/div[2]/div[1]/h3").inner_text()
            with open('linkendin.txt', 'w', encoding='utf-8') as file:
                  file.write("Linkendin De: " + pagina + "\n")
                  file.write("Informacion: " + informacion + "\n")
                  file.write("Seguidores: " + seguidores + "\n")
                  file.write("Tamaño: " + tamaño + "\n")
        except Exception as e:
            print(f"Error: {e}")
        finally:
             browser.close()

if __name__ == "__main__":
    asyncio.run(run('https://www.instagram.com/eltallerdetephy.gt/','','',''))