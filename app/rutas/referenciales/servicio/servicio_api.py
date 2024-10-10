from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.servicio.ServicioDao import ServicioDao

serviapi = Blueprint('serviapi', __name__)

# Trae todas las servicioes
@serviapi.route('/servicios', methods=['GET'])
def getServicios():
    serviciodao = ServicioDao()

    try:
        servicios = serviciodao.getServicios()

        return jsonify({
            'success': True,
            'data': servicios,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas los servicios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@serviapi.route('/servicios/<int:servicio_id>', methods=['GET'])
def getServicio(servicio_id):
    serviciodao = ServicioDao()

    try:
        servicios = serviciodao.getServiciosById(servicio_id)

        if servicios:
            return jsonify({
                'success': True,
                'data': servicios,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el Servicio con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener Servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva servicio
@serviapi.route('/servicios', methods=['POST'])
def addServicios():
    data = request.get_json()
    serviciodao = ServicioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion_servicio']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion_servicio = data['descripcion_servicio'].upper()
        servicio_id = serviciodao.guardarServicio(descripcion_servicio)
        if servicio_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': servicio_id, 'descripcion_servicio': descripcion_servicio},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el Servicio. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar el Servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@serviapi.route('/servicios/<int:servicio_id>', methods=['PUT'])
def updateServicio(servicio_id):
    data = request.get_json()
    serviciodao = ServicioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion_servicio']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion_servicio = data['descripcion_servicio']
    try:
        if serviciodao.updateServicio(servicio_id, descripcion_servicio.upper()):
            return jsonify({
                'success': True,
                'data': {'id': servicio_id, 'descripcion_servicio': descripcion_servicio},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el servicio con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar el servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@serviapi.route('/servicios/<int:servicio_id>', methods=['DELETE'])
def deleteServicio(servicio_id):
    serviciodao = ServicioDao()

    try:
        # Usar el retorno de eliminarservicio para determinar el éxito
        if serviciodao.deleteServicio(servicio_id):
            return jsonify({
                'success': True,
                'mensaje': f'servicio con ID {servicio_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el servicio con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar el servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500