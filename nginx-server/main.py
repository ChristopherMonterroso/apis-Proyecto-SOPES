from flask import Flask, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def generate_report_and_serve():
    print("Generando informe...")
    # Ruta donde se debe generar el archivo reports.html
    output_path = "/api_load/reports.html"

    # Ruta del script .sh
    script_path = "nginx-server/generate_report.sh"  # Reemplaza con la ruta real de tu script

    # Ejecutar el script .sh
    subprocess.run(["bash", script_path])

    # Mostrar el informe generado después de ejecutar el script
  
    return send_file(output_path, as_attachment=False)
  

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=6000)