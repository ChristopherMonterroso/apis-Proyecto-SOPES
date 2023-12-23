#!/bin/bash

# Ruta donde se debe generar el archivo reports.html


#verificar si exsite access.log
if [ -f /var/log/nginx/access.log ]; then
    echo "El archivo access.log existe"
else
    echo "El archivo access.log no existe"
fi
# Ejecutar el comando GoAccess y redirigir la salida al archivo
goaccess -f /var/log/nginx/access.log --log-format=COMBINED > reports.html
#imprmiir ruta del reports.html
output_path=$(pwd)/reports.html
echo "El informe se ha generado correctamente en $output_path"
# Verificar si la ejecución fue exitosa
if [ $? -eq 0 ]; then
    echo "El informe se ha generado correctamente en $output_path"
else
    echo "Hubo un error al generar el informe."
fi