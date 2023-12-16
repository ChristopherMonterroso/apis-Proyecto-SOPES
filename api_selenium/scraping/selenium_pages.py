import json
import asyncio
import time
import smtplib
import redis
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
redis_host = '192.168.1.41'
redis_port = 8000
redis_db = 0
pdf_content = "Reporte_Selenium.pdf"
pdf = SimpleDocTemplate(pdf_content, pagesize=letter)
content = []
async def run(instagram_url:str, facebook_url:str, twitter_url:str, linkedin_url:str):
    tasks = []
    error_report = []
    if instagram_url!="":
        tasks.append(asyncio.create_task(get_info_with_retry(get_info_instagram, instagram_url, error_report)))
    if facebook_url!="":
        tasks.append(asyncio.create_task(get_info_with_retry(get_info_facebook, facebook_url, error_report)))
    if twitter_url!="":
        tasks.append(asyncio.create_task(get_info_with_retry(get_info_twitter, twitter_url, error_report)))
    if linkedin_url!="":
        tasks.append(asyncio.create_task(get_info_with_retry(get_info_linkedin, linkedin_url, error_report)))

    await asyncio.gather(*tasks)
    generate_error_report_pdf(error_report)
    send_email("Selenium_error_report.pdf", "garciajonatan56@gmail.com")
    pdf.build(content)
    print("Se ha generado el informe en el archivo: Reporte_Selenium.pdf")
    send_email_report("Reporte_Selenium.pdf", "garciajonatan56@gmail.com")
    

async def get_info_instagram(url):
    # Set up the Chrome browser
    options = webdriver.ChromeOptions()
    
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
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
        print("informacion de instagram")
        print(pagina)
        print(informacion)
        print(posts)
        print(followers)
        print(followed)
        #crear pdf con la informacion
        add_text("Instagram De: " + pagina)
        data = [["Informacion", "Publicaciones", "Seguidores", "Seguidos"],[
            informacion, posts, followers, followed]]
        add_table(data)
        
        
        await save_to_redis(pagina, informacion, posts, followers, followed)
        
        with open('instagram.txt', 'w', encoding='utf-8') as file:
                file.write("Instagram De: " + pagina + "\n")
                file.write("Informacion: " + informacion + "\n")
                file.write("Publicaciones: " + posts + "\n")
                file.write("Seguidores: " + followers+ "\n")
                file.write("Seguidos: " + followed + "\n")
    finally:
        # Close the browser
        browser.quit()

async def get_info_facebook(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
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
        print("informacion de facebook")
        print(pagina)
        print(informacion)
        print(likes)
        print(seguidores)
        #crear pdf con la informacion
        add_text("Facebook De: " + pagina)
        data = [["Informacion", "Likes", "Seguidores"],[
            informacion, likes, seguidores]]
        add_table(data)
        
        await save_to_redis(pagina, informacion, likes, seguidores, "vacio")
        with open('facebook.txt', 'w', encoding='utf-8') as file:
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
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
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
        print("informacion de twitter")
        print(pagina)
        print(informacion)
        print(followers)
        print(followed)
        #crear pdf con la informacion
        add_text("Twitter De: " + pagina)
        data = [["Informacion", "Seguidores", "Seguidos"],[
            informacion, followers, followed]]
        add_table(data)
        await save_to_redis(pagina, informacion, followers, followed, "vacio")
        with open('twitter.txt', 'w', encoding='utf-8') as file:
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
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
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
        print("informacion de linkedin")
        print(pagina)
        print(informacion)
        print(tamano)
        print(seguidores)
        #crear pdf con la informacion
        add_text("Linkedin De: " + pagina)
        data = [["Informacion", "Tamano", "Seguidores"],[
            informacion, tamano, seguidores]]
        add_table(data)
        await save_to_redis(pagina, informacion, tamano, seguidores, "vacio")
        with open('linkedin.txt', 'w', encoding='utf-8') as file:
            file.write("Linkedin De: " + pagina + "\n")
            file.write("Informacion: " + informacion + "\n")
            file.write("tamano: " + tamano + "\n")
            file.write("Seguidores: " + seguidores + "\n")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        browser.quit()
        
async def save_to_redis(pagina, informacion, posts, followers, followed):
    try:
        lista_datos = []
        pagina = str(pagina)
        informacion = str(informacion)
        posts = str(posts)
        followers = str(followers)
        followed = str(followed)
        data = {
        'pagina': pagina,
        'informacion': informacion,
        'posts': posts,
        'followers': followers,
        'followed': followed
    }
        lista_datos.append(data)
        segundo = time.time()
        data_to_insert= [
         {'key': str(segundo),
             'value': json.dumps(lista_datos),
            },
        ]
        with ThreadPoolExecutor(max_workers=2) as executor:
    # Ejecutar las operaciones de inserción en Redis de manera paralela
            futures_insert = [executor.submit(insert_data_into_redis, data) for data in data_to_insert]
    # Esperar a que todas las operaciones de inserción se completen
            for future in futures_insert:
                future.result()
    except Exception as e:
        print(f"Error al almacenar en Redis: {e}")
        
def insert_data_into_redis(data):
    key = data['key']
    value = data['value']
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    try:
        r.set(key,value)
        print(f'{value} insertado en Redis correctamente')
    except Exception as e:
        print(f'Error al insertar {value} en Redis: {e}')

async def get_info_with_retry(get_info_function, url, error_report, max_retries=3, timeout=30):
    for retry in range(1, max_retries + 1):
        try:
            await asyncio.wait_for(get_info_function(url), timeout=timeout)

            # Si la función se ejecuta sin errores dentro del límite de tiempo, salir del bucle
            break
        except asyncio.TimeoutError:
            network = get_info_function.__name__.replace("get_info_", "").capitalize()
            add_error_to_report(error_report, network, f"Tiempo de espera agotado - Intento {retry}/{max_retries}")
            if retry == max_retries:
                print("Se alcanzó el número máximo de intentos.")
                break
            else:
                print("Reintentando...")
        except Exception as e:
            network = get_info_function.__name__.replace("get_info_", "").capitalize()
            add_error_to_report(error_report, network, f"Error - Intento {retry}/{max_retries}: {e}")
            if retry == max_retries:
                print("Se alcanzó el número máximo de intentos.")
                break
            else:
                print("Reintentando...")
def add_error_to_report(error_report, social_network, description):
   error_report.append({
        'Social Network': social_network,
        'Description': description,
        'Attempts': len(error_report) + 1  # Intentos hasta ahora
    })


def generate_error_report_pdf(error_report):
    pdf_filename = "Selenium_error_report.pdf"
    try:
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        elements = []

        # Encabezado de la tabla
        table_data = [["Red social", "Descripción del error", "Intentos"]]

        # Datos de la tabla
        for error in error_report:
            table_data.append([error['Social Network'], error['Description'], error['Attempts']])

        # Crear la tabla y aplicar estilo
        table = Table(table_data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        table.setStyle(style)
        elements.append(table)

        # Construir el PDF
        doc.build(elements)

        print(f"Se ha generado el informe de errores en el archivo: {pdf_filename}")
    except Exception as e:
        print(f"Error al generar el informe PDF: {e}")

def send_email(pdf_filename, recipient_email):
    sender_email = "sstmsprtvs@gmail.com"  # Reemplaza con tu dirección de correo electrónico
    sender_password = "mhgc cpin qdbs mgop"  # Reemplaza con la contraseña de tu correo electrónico

    subject = "Informe de Errores - Selenium"
    body = "Adjunto encontrarás el informe de errores generado por Selenium."

    # Crear el mensaje
    message = MIMEMultipart()
    message.attach(MIMEText(body, "plain"))
    
    # Adjuntar el PDF al mensaje
    with open(pdf_filename, "rb") as pdf_file:
        attach = MIMEApplication(pdf_file.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str(pdf_filename))
        message.attach(attach)

    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email

    # Establecer la conexión con el servidor SMTP de Gmail
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        
def send_email_report(pdf_filename, recipient_email):
    sender_email = "sstmsprtvs@gmail.com"  # Reemplaza con tu dirección de correo electrónico
    sender_password = "mhgc cpin qdbs mgop"  # Reemplaza con la contraseña de tu correo electrónico

    subject = "Informe de Paginas- Selenium"
    body = "Adjunto encontrarás el informe de paginas generado por Selenium."

    # Crear el mensaje
    message = MIMEMultipart()
    message.attach(MIMEText(body, "plain"))
    
    # Adjuntar el PDF al mensaje
    with open(pdf_filename, "rb") as pdf_file:
        attach = MIMEApplication(pdf_file.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str(pdf_filename))
        message.attach(attach)

    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email

    # Establecer la conexión con el servidor SMTP de Gmail
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        
def add_text(text):
    styles = getSampleStyleSheet()
    content.append(Paragraph(text, styles["Normal"]))

def add_table(data):
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    content.append(table)