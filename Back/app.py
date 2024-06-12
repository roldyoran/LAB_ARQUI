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

@app.route('/estado_luces', methods=['GET'])
def get_luces_state():
    return jsonify(estado_luces)

@app.route('/control_luz', methods=['POST'])
def control_luz():
    global estado_luces
    data = request.get_json()
    print(data)
    if 'habitacion' in data and 'encendido' in data:
        habitacion = data['habitacion']
        estado_luces[habitacion] = data['encendido']
    return jsonify(estado_luces)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
