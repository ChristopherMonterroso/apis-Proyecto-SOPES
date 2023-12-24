from flask import Flask, jsonify
import docker

app = Flask(__name__)

def convertir_bytes_a_megabytes(bytes_valor):
    return bytes_valor / (1024 * 1024)

def convertir_bytes_a_kilobytes(bytes_valor):
    return bytes_valor / (1024)

@app.route('/container_stats', methods=['GET'])
def get_container_stats():
    print("La solicitud ha sido recibida")
    cliente_docker = docker.from_env()
    nombre_contenedor = 'stupefied_thompson'  # Reemplaza con el nombre de tu contenedor
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
    return jsonify({
        'ram': {
            'uso': f"{convertir_bytes_a_megabytes(estadisticas_memoria['usage']):.2f} MB",
            'limite': f"{convertir_bytes_a_megabytes(estadisticas_memoria['limit']):.2f} MB",
            'porcentaje': f"{(estadisticas_memoria['usage'] / estadisticas_memoria['limit']) * 100:.2f}%"
        },
        'almacenamiento': {
            'memory_in': f"{memory_in:.2f} MB",
            'memory_out': f"{memory_out:.2f} KB",
            
        },
        'red': {
            'red_in': f"{red_in:.2f} KB",
            'red_out': f"{red_out:.2f} KB",
        },
        'cpu': {
            'porcentaje': f"{porcentaje_cpu:.2f}%"
        },
    })


if __name__ == '__main__':
    app.run(debug=True,port=8010)