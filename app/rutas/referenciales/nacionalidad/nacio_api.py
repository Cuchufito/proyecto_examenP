from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.nacionalidad.NacioDao import NacioDao

nacioapi = Blueprint('nacioapi', __name__)

# Trae todas las nacionalidades
@nacioapi.route('/nacionalidad', methods=['GET'])
def getNacionalidades():
    naciodao = NacioDao()

    try:
        nacionalidad = naciodao.getNacionalidades()

        return jsonify({
            'success': True,
            'data': nacionalidad,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las Nacionalidades: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@nacioapi.route('/nacionalidad/<int:nacio_id>', methods=['GET'])
def getNacionalidad(nacio_id):
    naciodao = NacioDao()

    try:
        nacionalidad = naciodao.getNacionalidadById(nacio_id)

        if nacionalidad:
            return jsonify({
                'success': True,
                'data': nacionalidad,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la Nacionalidad con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener Nacionalidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nueva nacionalidad
@nacioapi.route('/nacionalidad', methods=['POST'])
def addNacionalidad():
    data = request.get_json()
    naciodao = NacioDao()

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
        nacio_id = naciodao.guardarNacionalidad(descripcion)
        if nacio_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': nacio_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar la Naciconalidad. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar nacionalidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@nacioapi.route('/nacionalidad/<int:nacio_id>', methods=['PUT'])
def updateNacionalidad(nacio_id):
    data = request.get_json()
    naciodao = NacioDao()

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
        if naciodao.updateNacionalidad(nacio_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': nacio_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la Nacionalidad con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar la Nacionalidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@nacioapi.route('/nacionalidad/<int:nacio_id>', methods=['DELETE'])
def deleteNacionalidad(nacio_id):
    naciodao = NacioDao()

    try:
        # Usar el retorno de eliminarCiudad para determinar el éxito
        if naciodao.deleteNacionalidad(nacio_id):
            return jsonify({
                'success': True,
                'mensaje': f'Nacionalidad con ID {nacio_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la Nacionalidad con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar nacionalidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500