import asyncio
from playwright.async_api import async_playwright
from playwright._impl._errors import TargetClosedError
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import smtplib
import json
import time
import redis
from concurrent.futures import ThreadPoolExecutor
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
pdf_content = "Reporte_Playwright.pdf"
pdf = SimpleDocTemplate(pdf_content, pagesize=letter)
content = []
redis_host = '192.168.1.41'
redis_port = 8000
redis_db = 0
async def run(instagram_url, facebook_url, twitter_url, linkedin_url):
    tasks = []
    error_report = []
    if facebook_url != "":
        tasks.append(asyncio.create_task(get_info_with_retry(get_info_facebook, facebook_url, error_report)))
    if instagram_url!="":
        tasks.append(asyncio.create_task(get_info_with_retry(get_info_instagram, instagram_url, error_report)))
    if twitter_url!="":
        tasks.append(asyncio.create_task(get_info_with_retry(get_info_twitter, twitter_url, error_report)))
    if linkedin_url!="":
        tasks.append(asyncio.create_task(get_info_with_retry(get_info_linkedin, linkedin_url, error_report)))
    await asyncio.gather(*tasks)
    generate_error_report_pdf(error_report)
    send_email("Playwright_error_report.pdf", "garciajonatan56@gmail.com") 

async def get_info_instagram(url):
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=50,
            args=['--no-sandbox', '--disable-gpu', '--disable-software-rasterizer']
        )
       
        page = await browser.new_page()
        try:
            await page.goto('https://www.instagram.com/accounts/login/')
            await page.fill('input[name="username"]', 'sistemasoperativos1')
            await page.fill('input[name="password"]', 'Sopes123')
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(5000)
            await page.goto(url)
            await page.wait_for_timeout(5000)
            pagina = await page.locator("//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/a/h2").inner_text()
            informacion = await page.locator("//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/h1").inner_text()
            seguidores = await page.locator("//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span").inner_text()
            publicaciones = await page.locator("//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span").inner_text()
            seguidos = await page.locator("//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span").inner_text()
            add_text("Instagram De: " + pagina)
            data = [["Informacion", "Publicaciones", "Seguidores", "Seguidos"],[
            informacion, publicaciones, seguidores, seguidos]]
            add_table(data)
        
        
            await save_to_redis(pagina, informacion, publicaciones, seguidores,seguidos)
            with open('instagram.txt', 'w', encoding='utf-8') as file:
                file.write("Instagram De: " + pagina + "\n")
                file.write("Informacion: " + informacion + "\n")
                file.write("Publicaciones: " + publicaciones + "\n")
                file.write("Seguidores: " + seguidores + "\n")
                file.write("Seguidos: " + seguidos + "\n")
                

        finally:
            if browser:
                # Cerrar la página antes de cerrar el navegador
                await page.close()
                # Cerrar el navegador
                await browser.close()

async def get_info_facebook(url):
   async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=50,
            args=['--no-sandbox', '--disable-gpu', '--disable-software-rasterizer']
        )
        print("va bien en twitter")
        page = await browser.new_page()
        try:
           await page.goto(url)
           pagina = await page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/div/div/span/h1").inner_text()                  
           seguidores = await page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[2]").inner_text()
           likes = await page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[1]").inner_text()
           informacion = await page.locator("//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/span").inner_html()     
           add_text("Instagram De: " + pagina)
           data = [["Informacion", "seguidores", "likes"],[
           informacion, seguidores, seguidores, likes]]
           add_table(data)
        
        
           await save_to_redis(pagina, informacion, likes, seguidores,"vacio")    
           with open('facebook.txt', 'w', encoding='utf-8') as file:
                file.write("Facebook De: " + pagina + "\n")
                file.write("Informacion: " + informacion + "\n")
                file.write("likes: " + likes + "\n")
                file.write("Seguidores: " + seguidores + "\n")
        finally:
            if browser:
                # Cerrar la página antes de cerrar el navegador
                await page.close()
                # Cerrar el navegador
                await browser.close()



async def get_info_twitter(url):
     async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50,args=['--no-sandbox', '--disable-gpu', '--disable-software-rasterizer'])
        page = await browser.new_page()
        try:
            await page.goto('https://twitter.com/i/flow/login')
            await page.fill('input[name="text"]', 'SistemasOp1')
            await page.locator("//html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]").click()
            await page.fill('input[name="password"]', 'sistemasoperativos1')
            await page.locator("//html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div").click()
            await page.goto(url)
            pagina = await page.locator("//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span/span[1]").inner_text()
            informacion = await page.locator("//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[3]/div/div[1]/span").inner_text()
            seguidores = await page.locator("//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span").inner_text()
            seguidos = await page.locator("//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span").inner_text()
            #agregar a pdf
            add_text("Twitter De: " + pagina)
            data = [["Informacion", "seguidores", "seguidos"],[
            informacion, seguidores, seguidos]]
            add_table(data)
            #agregar a redis
            await save_to_redis(pagina, informacion, seguidores, seguidos,"vacio")
            with open('twitter.txt', 'w', encoding='utf-8') as file:
                  file.write("Twiter De: " + pagina + "\n")
                  file.write("Informacion: " + informacion + "\n")
                  file.write("Seguidores: " + seguidores + "\n")
                  file.write("Seguidos: " + seguidos + "\n")

        finally:
            if browser:
                # Cerrar la página antes de cerrar el navegador
                await page.close()
                # Cerrar el navegador
                await browser.close()
    
async def get_info_linkedin(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50,args=['--no-sandbox', '--disable-gpu', '--disable-software-rasterizer'])
        page = await browser.new_page()
        try:
            await page.goto(url)
            pagina = await page.locator("//html/body/main/section[1]/section/div/div[2]/div[1]/h1").inner_text()
            informacion = await page.locator("//html/body/main/section[1]/section/div/div[2]/div[1]/h2").inner_text()
            tamaño = await page.locator("//html/body/main/section[1]/div/section[1]/div/dl/div[3]/dd").inner_text()
            seguidores= await page.locator("//html/body/main/section[1]/section/div/div[2]/div[1]/h3").inner_text()
            #agregar a pdf
            add_text("Linkendin De: " + pagina)
            data = [["Informacion", "seguidores", "tamaño"],[
            informacion, seguidores, tamaño]]
            add_table(data)
            #agregar a redis
            await save_to_redis(pagina, informacion, seguidores, tamaño,"vacio")
            with open('linkendin.txt', 'w', encoding='utf-8') as file:
                  file.write("Linkendin De: " + pagina + "\n")
                  file.write("Informacion: " + informacion + "\n")
                  file.write("Seguidores: " + seguidores + "\n")
                  file.write("Tamaño: " + tamaño + "\n")
        finally:
            if browser:
                # Cerrar la página antes de cerrar el navegador
                await page.close()
                # Cerrar el navegador
                await browser.close()
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
        except TargetClosedError as s:
            network = get_info_function.__name__.replace("get_info_", "").capitalize()
            add_error_to_report(error_report, network, f"El objetivo se cerró durante - Intento {retry}/{max_retries}")
            if retry == max_retries:
                print("Se alcanzó el número máximo de intentos.")
                break
            else:
                print("Reintentando...")
                await asyncio.sleep(2)
        except Exception as e:
            network = get_info_function.__name__.replace("get_info_", "").capitalize()
            add_error_to_report(error_report, network, f"Error - Intento {retry}/{max_retries}: {e}")
            if retry == max_retries:
                add_error_to_report(error_report, get_info_function.__name__, f"Se alcanzó el número máximo de intentos.")
                break
            else:
                print("Reintentando...")
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

def add_error_to_report(error_report, social_network, description):
   error_report.append({
        'Social Network': social_network,
        'Description': description,
        'Attempts': len(error_report) + 1  # Intentos hasta ahora
    })

def generate_error_report_pdf(error_report):
    pdf_filename = "Playwright_error_report.pdf"
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

    subject = "Informe de Errores - Playwright"
    body = "Adjunto encontrarás el informe de errores generado por Playwright."

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
if __name__ == "__main__":
    asyncio.run(run('','http://www.facebook.com/kemgt/','',''))