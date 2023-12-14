FROM alpine:3.10

# Install packages para trabajar con selenium flask python
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip 

RUN apk --no-cache add \
    wget \
    unzip \
    chromium

# Descargar y descomprimir Chromedriver
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.71/linux64/chromedriver-linux64.zip  \
&& unzip chromedriver-linux64.zip 
  

# Mover Chromedriver al directorio en el PATH
RUN mv chromedriver-linux64 /usr/local/bin/
#actualizar chromedriver


# Configura Chromedriver en PATH
ENV PATH="/usr/lib/chromium/chromedriver:${PATH}"

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

#ejecutar dentro de Selenium_api main.py
CMD ["python3", "api_selenium/main.py"]