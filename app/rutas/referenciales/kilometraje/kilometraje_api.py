from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.kilometraje.KilometrajeDao import KilometrajeDao

kiloapi = Blueprint('kiloapi', __name__)

# Trae todos los kilometrajes
@kiloapi.route('/kilometrajes', methods=['GET'])
def getKilometrajes():
    kilodao = KilometrajeDao()

    try:
        kilometrajes = kilodao.getKilometrajes()

        return jsonify({
            'success': True,
            'data': kilometrajes,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los kilometrajes: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@kiloapi.route('/kilometrajes/<int:kilometraje_id>', methods=['GET'])
def getKilometraje(kilometraje_id):
    kilodao = KilometrajeDao()

    try:
        kilometraje = kilodao.getKilometrajeById(kilometraje_id)

        if kilometraje:
            return jsonify({
                'success': True,
                'data': kilometraje,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el kilometraje con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener kilometraje: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo kilometraje
@kiloapi.route('/kilometrajes', methods=['POST'])
def addKilometrajeDao():
    data = request.get_json()
    kilodao = KilometrajeDao()

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
        kilometraje_id = kilodao.guardarKilometraje(descripcion)
        if kilometraje_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': kilometraje_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el kilometraje. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar kilometraje: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@kiloapi.route('/kilometrajes/<int:kilometraje_id>', methods=['PUT'])
def updateKilometraje(kilometraje_id):
    data = request.get_json()
    kilodao = KilometrajeDao()

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
        if kilodao.updateKilometraje(kilometraje_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': kilometraje_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el kilometraje con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar kilometraje: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@kiloapi.route('/kilometrajes/<int:kilometraje_id>', methods=['DELETE'])
def deleteKilometraje(kilometraje_id):
    kilodao = KilometrajeDao()

    try:
        # Usar el retorno de eliminarKilometrajeDao para determinar el éxito
        if kilodao.deleteKilometraje(kilometraje_id):
            return jsonify({
                'success': True,
                'mensaje': f'Kilometraje con ID {kilometraje_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el kilometraje con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar kilometraje: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
