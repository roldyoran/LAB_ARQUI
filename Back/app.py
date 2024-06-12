from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Estado inicial de las luces en cada habitación
estado_luces = {
    'recepcion': False,
    'conferencias': False,
    'trabajo': False,
    'administrativa': False,
    'carga_descarga': False,
    'cafeteria': False,
    'bano': False,
    'exterior': False
}

codigo_binario_luces = {
    'recepcion':        [0,0,0],
    'conferencias':     [0,0,1],
    'trabajo':          [0,1,0],
    'administrativa':   [0,1,1],
    'carga_descarga':   [1,0,0],
    'cafeteria':        [1,0,1],
    'bano':             [1,1,0],
    'exterior':         [1,1,1]
}


@app.route('/estado_luces', methods=['GET'])
def get_luces_state():
    return jsonify(estado_luces)

@app.route('/apagar_puertos', methods=['POST'])
def get_luces_state():
    # Aqui se apagan los puertos
    puertos_apagados = {
        'puertos_apagados': False,
    }
    return jsonify(puertos_apagados)


@app.route('/control_luz', methods=['POST'])
def control_luz():
    global estado_luces
    data = request.get_json()
    print(data)
    if 'habitacion' in data and 'encendido' in data:
        habitacion = data['habitacion']
        estado_luces[habitacion] = data['encendido']
        if data['encendido']:
            print(f"GPIO.puerto1: {(codigo_binario_luces[habitacion])[0]}")
            print(f"GPIO.puerto2: {(codigo_binario_luces[habitacion])[1]}")
            print(f"GPIO.puerto3: {(codigo_binario_luces[habitacion])[2]}")


    return jsonify(estado_luces)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
