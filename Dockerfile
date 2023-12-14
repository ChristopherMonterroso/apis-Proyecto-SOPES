FROM alpine:3.19.0


RUN apk add --no-cache python3-dev py3-pip
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip3 install --upgrade pip

RUN apk add chromium 
RUN apk add chromium-chromedriver

RUN chromedriver --version

WORKDIR /Selenium_api

#copiar solo api_selenium luego 
COPY api_selenium api_selenium
#copiar requirements se encuentra en la misma linea que este dockerfile
COPY requirements.txt requirements.txt

RUN pip --no-cache-dir install -r requirements.txt
# Playwright

RUN pip3 install --upgrade pip
# RUN pip3 install playwright
RUN pip3 install selenium
RUN pip3 install --upgrade Flask Jinja2




# Descargar el chromedriver




#ejecutar dentro de Selenium_api main.py
CMD ["python3", "api_selenium/main.py"]