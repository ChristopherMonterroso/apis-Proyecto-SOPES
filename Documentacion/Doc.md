# UNIVERSIDAD DE SAN CARLOS DE GUATEMALA 
# FACULTAD DE INGENIERIA 
# ESCUELA DE CIENCIAS Y SISTEMAS 
# SISTEMAS OPERATIVOS 1

| Nombre       | Carnet  |
|--------------|--------------|
| Kemel Josué Efraín Ruano Jerónimo     | 202006373|
| Jonatan Leonel García Arana           | 201902363   |
| Christopher Iván Monterroso Alegria    | 202000424 |

## API - Selenium
### Endpoint Configuracion
![Texto alternativo](Images\selenium.png)
## API - Playwright
### Endpoint Configuracion
![Texto alternativo](Images\play.png)

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