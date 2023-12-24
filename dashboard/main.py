from flask import Flask, jsonify,request
import docker
from flask_cors import CORS
app = Flask(__name__)
#AGREGAR CORS
CORS(app)
def convertir_bytes_a_megabytes(bytes_valor):
    return bytes_valor / (1024 * 1024)

def convertir_bytes_a_kilobytes(bytes_valor):
    return bytes_valor / (1024)

@app.route('/container_selenium', methods=['GET'])
def get_container_stats_selenium():
   try:
    print("La solicitud ha sido recibida")
    cliente_docker = docker.from_env()
    nombre_contenedor = 'selenium'  # Reemplaza con el nombre de tu contenedor
    contenedor = cliente_docker.containers.get(nombre_contenedor)
    estadisticas = contenedor.stats(stream=True, decode=True)
    primera_actualizacion = next(estadisticas)
    estadisticas_memoria = primera_actualizacion['memory_stats']
    estadisticas_almacenamiento = primera_actualizacion['blkio_stats']
    porcentaje_cpu = primera_actualizacion['cpu_stats']['cpu_usage']['total_usage'] / primera_actualizacion['cpu_stats']['system_cpu_usage'] * 100
    pids = primera_actualizacion['pids_stats']['current']
    estadisticas_block_io = primera_actualizacion['blkio_stats']['io_service_bytes_recursive']
    memory_in = primera_actualizacion['blkio_stats']['io_service_bytes_recursive'][0]['value']
    memory_out = primera_actualizacion['blkio_stats']['io_service_bytes_recursive'][1]['value']
    memory_in = convertir_bytes_a_megabytes(memory_in)
    memory_out = convertir_bytes_a_kilobytes(memory_out)
    red_in = primera_actualizacion['networks']['eth0']['rx_bytes']
    red_out = primera_actualizacion['networks']['eth0']['rx_dropped']
    red_in = convertir_bytes_a_kilobytes(red_in)
    red_out = convertir_bytes_a_kilobytes(red_out)
    print(estadisticas)
    return jsonify({
        'ram': {
            'uso': f"{convertir_bytes_a_megabytes(estadisticas_memoria['usage']):.2f} ",#MB
            'limite': f"{convertir_bytes_a_megabytes(estadisticas_memoria['limit']):.2f} ",#MB
            'porcentaje': f"{(estadisticas_memoria['usage'] / estadisticas_memoria['limit']) * 100:.2f}"#%
        },
        'almacenamiento': {
            'memory_in': f"{memory_in:.2f} ",#MB
            'memory_out': f"{memory_out:.2f} ",#KB
            
        },
        'red': {
            'red_in': f"{red_in:.2f} ", #KB
            'red_out': f"{red_out:.2f} ", #KB
        },
        'cpu': {
            'porcentaje': f"{porcentaje_cpu:.2f}" #%
        },
    })
   except:
        cliente_docker = docker.from_env()
        nombre_contenedor = 'selenium'  # Reemplaza con el nombre de tu contenedor
        contenedor = cliente_docker.containers.get(nombre_contenedor)
        estadisticas = contenedor.stats(stream=True, decode=True)
        primera_actualizacion = next(estadisticas)
        estadisticas_memoria = primera_actualizacion['memory_stats']
        red_in = primera_actualizacion['networks']['eth0']['rx_bytes']
        red_out = primera_actualizacion['networks']['eth0']['rx_dropped']
        red_in = convertir_bytes_a_kilobytes(red_in)
        red_out = convertir_bytes_a_kilobytes(red_out)
        estadisticas_almacenamiento = primera_actualizacion['blkio_stats']
        porcentaje_cpu = primera_actualizacion['cpu_stats']['cpu_usage']['total_usage'] / primera_actualizacion['cpu_stats']['system_cpu_usage'] * 100
        return jsonify({
        'ram': {
            'uso': f"{convertir_bytes_a_megabytes(estadisticas_memoria['usage']):.2f} ",#MB
            'limite': f"{convertir_bytes_a_megabytes(estadisticas_memoria['limit']):.2f} ",#MB
            'porcentaje': f"{(estadisticas_memoria['usage'] / estadisticas_memoria['limit']) * 100:.2f}"#%
        },
        'almacenamiento': {
            'memory_in': f"0",#MB
            'memory_out': f"0",#KB
        },
        'red': {
            'red_in': f"{red_in:.2f} ", #KB
            'red_out': f"{red_out:.2f} ", #KB
        },
        'cpu': {
            'porcentaje': f"{porcentaje_cpu:.2f}" #%
        },
    })

@app.route('/container_playwright', methods=['GET'])
def get_container_stats_playwright():
    print("La solicitud ha sido recibida")
    cliente_docker = docker.from_env()
    nombre_contenedor = 'playwright'  # Reemplaza con el nombre de tu contenedor
    contenedor = cliente_docker.containers.get(nombre_contenedor)
    estadisticas = contenedor.stats(stream=True, decode=True)
    primera_actualizacion = next(estadisticas)
    estadisticas_memoria = primera_actualizacion['memory_stats']
    estadisticas_almacenamiento = primera_actualizacion['blkio_stats']
    porcentaje_cpu = primera_actualizacion['cpu_stats']['cpu_usage']['total_usage'] / primera_actualizacion['cpu_stats']['system_cpu_usage'] * 100
    pids = primera_actualizacion['pids_stats']['current']
    estadisticas_block_io = primera_actualizacion['blkio_stats']['io_service_bytes_recursive']
    memory_in = primera_actualizacion['blkio_stats']['io_service_bytes_recursive'][0]['value']
    memory_out = primera_actualizacion['blkio_stats']['io_service_bytes_recursive'][1]['value']
    memory_in = convertir_bytes_a_megabytes(memory_in)
    memory_out = convertir_bytes_a_kilobytes(memory_out)
    red_in = primera_actualizacion['networks']['eth0']['rx_bytes']
    red_out = primera_actualizacion['networks']['eth0']['rx_dropped']
    red_in = convertir_bytes_a_kilobytes(red_in)
    red_out = convertir_bytes_a_kilobytes(red_out)
    print(estadisticas)
    return jsonify({
        'ram': {
            'uso': f"{convertir_bytes_a_megabytes(estadisticas_memoria['usage']):.2f} ",#MB
            'limite': f"{convertir_bytes_a_megabytes(estadisticas_memoria['limit']):.2f} ",#MB
            'porcentaje': f"{(estadisticas_memoria['usage'] / estadisticas_memoria['limit']) * 100:.2f}"#%
        },
        'almacenamiento': {
            'memory_in': f"{memory_in:.2f} ",#MB
            'memory_out': f"{memory_out:.2f} ",#KB
            
        },
        'red': {
            'red_in': f"{red_in:.2f} ", #KB
            'red_out': f"{red_out:.2f} ", #KB
        },
        'cpu': {
            'porcentaje': f"{porcentaje_cpu:.2f}" #%
        },
    })
    
@app.route('/container_redis', methods=['GET'])
def get_container_stats_redis():
    print("La solicitud ha sido recibida")
    cliente_docker = docker.from_env()
    nombre_contenedor = 'redis'  # Reemplaza con el nombre de tu contenedor
    contenedor = cliente_docker.containers.get(nombre_contenedor)
    estadisticas = contenedor.stats(stream=True, decode=True)
    primera_actualizacion = next(estadisticas)
    estadisticas_memoria = primera_actualizacion['memory_stats']
    estadisticas_almacenamiento = primera_actualizacion['blkio_stats']
    porcentaje_cpu = primera_actualizacion['cpu_stats']['cpu_usage']['total_usage'] / primera_actualizacion['cpu_stats']['system_cpu_usage'] * 100
    pids = primera_actualizacion['pids_stats']['current']
    estadisticas_block_io = primera_actualizacion['blkio_stats']['io_service_bytes_recursive']
    memory_in = primera_actualizacion['blkio_stats']['io_service_bytes_recursive'][0]['value']
    memory_out = primera_actualizacion['blkio_stats']['io_service_bytes_recursive'][1]['value']
    memory_in = convertir_bytes_a_megabytes(memory_in)
    memory_out = convertir_bytes_a_kilobytes(memory_out)
    red_in = primera_actualizacion['networks']['eth0']['rx_bytes']
    red_out = primera_actualizacion['networks']['eth0']['rx_dropped']
    red_in = convertir_bytes_a_kilobytes(red_in)
    red_out = convertir_bytes_a_kilobytes(red_out)
    print(estadisticas)
    return jsonify({
        'ram': {
            'uso': f"{convertir_bytes_a_megabytes(estadisticas_memoria['usage']):.2f} ",#MB
            'limite': f"{convertir_bytes_a_megabytes(estadisticas_memoria['limit']):.2f} ",#MB
            'porcentaje': f"{(estadisticas_memoria['usage'] / estadisticas_memoria['limit']) * 100:.2f}"#%
        },
        'almacenamiento': {
            'memory_in': f"{memory_in:.2f} ",#MB
            'memory_out': f"{memory_out:.2f} ",#KB
            
        },
        'red': {
            'red_in': f"{red_in:.2f} ", #KB
            'red_out': f"{red_out:.2f} ", #KB
        },
        'cpu': {
            'porcentaje': f"{porcentaje_cpu:.2f}" #%
        },
    })
    
@app.route('/container_ngnix', methods=['GET'])
def get_container_stats_ngnix():
    print("La solicitud ha sido recibida")
    cliente_docker = docker.from_env()
    nombre_contenedor = 'nginx'  # Reemplaza con el nombre de tu contenedor
    contenedor = cliente_docker.containers.get(nombre_contenedor)
    estadisticas = contenedor.stats(stream=True, decode=True)
    primera_actualizacion = next(estadisticas)
    estadisticas_memoria = primera_actualizacion['memory_stats']
    estadisticas_almacenamiento = primera_actualizacion['blkio_stats']
    porcentaje_cpu = primera_actualizacion['cpu_stats']['cpu_usage']['total_usage'] / primera_actualizacion['cpu_stats']['system_cpu_usage'] * 100
    pids = primera_actualizacion['pids_stats']['current']
    estadisticas_block_io = primera_actualizacion['blkio_stats']['io_service_bytes_recursive']
    memory_in = primera_actualizacion['blkio_stats']['io_service_bytes_recursive'][0]['value']
    memory_out = primera_actualizacion['blkio_stats']['io_service_bytes_recursive'][1]['value']
    memory_in = convertir_bytes_a_megabytes(memory_in)
    memory_out = convertir_bytes_a_kilobytes(memory_out)
    red_in = primera_actualizacion['networks']['eth0']['rx_bytes']
    red_out = primera_actualizacion['networks']['eth0']['rx_dropped']
    red_in = convertir_bytes_a_kilobytes(red_in)
    red_out = convertir_bytes_a_kilobytes(red_out)
    print(estadisticas)
    return jsonify({
        'ram': {
            'uso': f"{convertir_bytes_a_megabytes(estadisticas_memoria['usage']):.2f} ",#MB
            'limite': f"{convertir_bytes_a_megabytes(estadisticas_memoria['limit']):.2f} ",#MB
            'porcentaje': f"{(estadisticas_memoria['usage'] / estadisticas_memoria['limit']) * 100:.2f}"#%
        },
        'almacenamiento': {
            'memory_in': f"{memory_in:.2f} ",#MB
            'memory_out': f"{memory_out:.2f} ",#KB
            
        },
        'red': {
            'red_in': f"{red_in:.2f} ", #KB
            'red_out': f"{red_out:.2f} ", #KB
        },
        'cpu': {
            'porcentaje': f"{porcentaje_cpu:.2f}" #%
        },
    })
    
@app.route('/container_start', methods=['POST'])
def iniciar_contenedor():
    nombre = request.get_json()
    nombre = nombre['contenedor']
    cliente_docker = docker.from_env()
    contenedor = cliente_docker.containers.get(nombre)
    #verificar si el contenedor esta corriendo
    print(contenedor.status)
    if contenedor.status == 'running':
        print("El contenedor ya esta corriendo")
        return jsonify({
            'status': 200,
            'mensaje': 'El contenedor ya esta corriendo'
        })
    else:
        contenedor.start()
        return jsonify({
            'status': 400,
            'mensaje': 'Contenedor iniciado'
        })
 
    
if __name__ == '__main__':
    app.run(debug=True,port=8010)