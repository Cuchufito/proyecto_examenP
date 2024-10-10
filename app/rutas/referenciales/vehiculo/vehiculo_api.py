from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.vehiculo.VehiculoDao import VehiculoDao

veapi = Blueprint('veapi', __name__)

# Trae todas las vehiculos
@veapi.route('/vehiculos', methods=['GET'])
def getVehiculos():
    vehiculodao = VehiculoDao()

    try:
        vehiculos = vehiculodao.getVehiculos()

        return jsonify({
            'success': True,
            'data': vehiculos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los vehiculos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@veapi.route('/vehiculos/<int:vehiculo_id>', methods=['GET'])
def getVehiculo(vehiculo_id):
    vehiculodao = VehiculoDao()

    try:
        vehiculo = vehiculodao.getVehiculoById(vehiculo_id)

        if vehiculo:
            return jsonify({
                'success': True,
                'data': vehiculo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el vehiculo con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener el vehiculo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo Vehiculo
@veapi.route('/vehiculos', methods=['POST'])
def addVehiculo():
    data = request.get_json()
    vehiculodao = VehiculoDao()

    campos_requeridos = ['marca', 'modelo']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        marca = data['marca'].upper()
        modelo = data['modelo'].upper()
        vehiculo_id = vehiculodao.guardarVehiculo(marca, modelo)
        if vehiculo_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': vehiculo_id, 'marca': marca, 'modelo': modelo},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el vehiculo. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar vehiculo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@veapi.route('/vehiculos/<int:vehiculo_id>', methods=['PUT'])
def updateVehiculo(vehiculo_id):
    data = request.get_json()
    vehiculodao = VehiculoDao()

    campos_requeridos = ['marca', 'modelo']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    marca = data['marca']
    modelo = data['modelo']

    try:
        if vehiculodao.updateVehiculo(vehiculo_id, marca.upper(), modelo.upper()):
            return jsonify({
                'success': True,
                'data': {'id': vehiculo_id, 'marca': marca, 'modelo': modelo},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el vehiculo con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar vehiculo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@veapi.route('/vehiculos/<int:vehiculo_id>', methods=['DELETE'])
def deleteVehiculo(vehiculo_id):
    vehiculodao = VehiculoDao()

    try:
        if vehiculodao.deleteVehiculo(vehiculo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Vehiculo con ID {vehiculo_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el vehiculo con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar vehiculo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
