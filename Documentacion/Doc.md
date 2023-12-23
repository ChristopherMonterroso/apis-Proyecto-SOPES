# UNIVERSIDAD DE SAN CARLOS DE GUATEMALA 
# FACULTAD DE INGENIERIA 
# ESCUELA DE CIENCIAS Y SISTEMAS 
# SISTEMAS OPERATIVOS 1

| Nombre       | Carnet  |
|--------------|--------------|
| Kemel Josué Efraín Ruano Jerónimo     | 202006373|
| Christopher Iván Monterroso Alegria         | 201902363   |
| Jonatan Leonel García Arana     | 202000424 |

## API - Selenium
### Endpoint Configuracion
![Texto alternativo](/Documentacion/Images/selenium.jpg)
## API - Playwright
### Endpoint Configuracion
![Texto alternativo](/Documentacion/Images/play.jpg)

## Docker - Selenium
### Configuracion
* FROM alpine:3.19.0
* RUN apk add --no-cache python3-dev py3-pip
* RUN python3 -m venv /venv
* ENV PATH="/venv/bin:$PATH"
* RUN pip3 install --upgrade pip
* RUN apk add chromium 
* RUN apk add chromium-chromedriver
* RUN chromedriver --version
* WORKDIR /Selenium_api
* COPY api_selenium api_selenium
* dockerfile
* COPY requirements.txt requirements.txt
* RUN pip --no-cache-dir install -r requirements.txt
* Playwright
* RUN pip3 install --upgrade pip
* RUN pip3 install selenium
* RUN pip3 install --upgrade Flask Jinja2
* RUN pip install redis
* RUN pip install reportlab
* CMD ["python3", "api_selenium/main.py"]
## Docker - Playwright
### Configuracion
* FROM mcr.microsoft.com/playwright:v1.40.0-jammy
* RUN apt-get update && apt-get install -y --no-install-recommends \libglib2.0-0
* RUN apt-get install -y --no-install-recommends python3 
* RUN apt-get install -y --no-install-recommends python3-pip 
* RUN apt-get install -y --no-install-recommends chromium-browser
* RUN rm -rf /var/lib/apt/lists/*
* RUN python3 -m pip install --upgrade pip
* WORKDIR /Playwright_api
* COPY api_playwright api_playwright
* WORKDIR /Playwright_api/api_playwright/chromedriver-linux64
* RUN mv chromedriver /usr/local/bin
* WORKDIR /Playwright_api
* COPY requirements.txt requirements.txt
* RUN pip3 install -r requirements.txt
* RUN pip3 install --upgrade selenium Flask Jinja2
* RUN pip3 install --upgrade playwright
* RUN playwright install
* RUN pip3 install redis
* RUN pip3 install reportlab
* CMD ["python3", "api_playwright/main.py"]

# FASE 2 
## Docker - LoadBalancer
### Configuracion
* FROM alpine:3.19.0
* RUN apk add --no-cache python3-dev py3-pip
* RUN python3 -m venv /venv
* ENV PATH="/venv/bin:$PATH"
* RUN pip3 install --upgrade pip
* RUN apk add nginx
* RUN apk add goaccess
* RUN apk add --no-cache bash
* RUN pip3 install --upgrade Flask Jinja2
* WORKDIR /api_load
* COPY nginx-server nginx-server
* COPY nginx-server/conf/nginx.conf /etc/nginx/
* WORKDIR /api_load
* CMD ["sh", "-c", "python3 nginx-server/main.py & nginx -g 'daemon off;'"]

## API - LoadBalancer
### Endpoint Configuracion
![Texto alternativo](/Documentacion/Images/reporteLoad.PNG)

### Configuracion de gnix
- ver el siguiente archivo **nginx.conf**


## Pruebas de Carga 
### Uso de Apache Bench
Para generar lo siguiente se necesita instalar **Apache Bench** 
- sudo apt install apache2-utils
Se ejecuta el siguiente comando una vez instalado 

- ab -g resultado.csv -c 4 -n 4 -p prueba.json -T "application/json" -s 300  http://localhost:9090/api/domain-social-info

![Texto alternativo](/Documentacion/Images/Captura.PNG)

### Imagenes para ver como fue la concurrencia de cada prueba que se realizo en este caso fueron 2

Primera prueba
![Texto alternativo](/Documentacion/Images/Captura3.PNG)
Segunda prueba
![Texto alternativo](/Documentacion/Images/Captura4.PNG)
