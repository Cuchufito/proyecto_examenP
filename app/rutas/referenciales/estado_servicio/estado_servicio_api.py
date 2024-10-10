from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.estado_servicio.EstadoServicioDao import EstadoServicioDao

estaserviapi = Blueprint('estaserviapi', __name__)

# Trae todos los Estados del servicio
@estaserviapi.route('/estadoservicio', methods=['GET'])
def getEstadoServicio():
    estadoserviciodao = EstadoServicioDao()

    try:
        estadosServicios = estadoserviciodao.getEstadoServicio()

        return jsonify({
            'success': True,
            'data': estadosServicios,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los Estados del servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@estaserviapi.route('/estadoservicio/<int:estadoservicio_id>', methods=['GET'])
def getEstadoServicioById(estadoservicio_id):
    estadoserviciodao = EstadoServicioDao()

    try:
        estadoservicio = estadoserviciodao.getEstadoServicioById(estadoservicio_id)

        if estadoservicio:
            return jsonify({
                'success': True,
                'data': estadoservicio,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado del servicio con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener estado del Servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega uno nuevo Estado del servicio 
@estaserviapi.route('/estadoservicio', methods=['POST'])
def addEstadoServicio():
    data = request.get_json()
    estadoserviciodao = EstadoServicioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion_estado']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion_estado = data['descripcion_estado'].upper()
        estadoservicio_id = estadoserviciodao.guardarEstadoServicio(descripcion_estado)
        if estadoservicio_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': estadoservicio_id, 'descripcion_estado': descripcion_estado},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el Estado del servicio. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar Estado del Servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@estaserviapi.route('/estadoservicio/<int:estadoservicio_id>', methods=['PUT'])
def updateEstadoServicio(estadoservicio_id):
    data = request.get_json()
    estadoserviciodao = EstadoServicioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion_estado']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion_estado = data['descripcion_estado']
    try:
        if estadoserviciodao.updateEstadoServicio(estadoservicio_id, descripcion_estado.upper()):
            return jsonify({
                'success': True,
                'data': {'id': estadoservicio_id, 'descripcion_estado': descripcion_estado},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado del servicio con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar Estado del sservicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@estaserviapi.route('/estadoservicio/<int:estadoservicio_id>', methods=['DELETE'])
def deleteEstadoServicio(estadoservicio_id):
    estadoserviciodao = EstadoServicioDao()

    try:
        # Usar el retorno de eliminarEstadoServicio para determinar el éxito
        if estadoserviciodao.deleteEstadoServicio(estadoservicio_id):
            return jsonify({
                'success': True,
                'mensaje': f'EstadoServicio con ID {estadoservicio_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado del servicio con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar Estado del servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500