from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.placa.PlacaDao import PlacaDao

placapi = Blueprint('placapi', __name__)

# Trae todas las placas de las personas
@placapi.route('/placas', methods=['GET'])
def getPlacas():
    placadao = PlacaDao()

    try:
        placas = placadao.getPlacas()

        return jsonify({
            'success': True,
            'data': placas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las placas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@placapi.route('/placas/<int:placa_id>', methods=['GET'])
def getPlaca(placa_id):
    placadao = PlacaDao()

    try:
        placa = placadao.getPlacaById(placa_id)

        if placa:
            return jsonify({
                'success': True,
                'data': placa,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el placa con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener placa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nuevo placa de la persona
@placapi.route('/placas', methods=['POST'])
def addPlaca():
    data = request.get_json()
    placadao = PlacaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        placa_id = placadao.guardarPlaca(descripcion)
        if placa_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': placa_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el placa. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar placa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@placapi.route('/placas/<int:placa_id>', methods=['PUT'])
def updatePlaca(placa_id):
    data = request.get_json()
    placadao = PlacaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    try:
        if placadao.updatePlaca(placa_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': placa_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el placa con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar placa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@placapi.route('/placas/<int:placa_id>', methods=['DELETE'])
def deletePlaca(placa_id):
    placadao = PlacaDao()

    try:
        # Usar el retorno de eliminarPlaca para determinar el éxito
        if placadao.deletePlaca(placa_id):
            return jsonify({
                'success': True,
                'mensaje': f'Placa con ID {placa_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el placa con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar placa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500