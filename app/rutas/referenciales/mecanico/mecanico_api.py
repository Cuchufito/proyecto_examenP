from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.mecanico.MecanicoDao import MecanicoDao

mecapi = Blueprint('mecapi', __name__)

# Trae todas las mecanico
@mecapi.route('/mecanicos', methods=['GET'])
def getMecanicos():
    mecanicodao = MecanicoDao()

    try:
        mecanicos = mecanicodao.getMecanicos()

        return jsonify({
            'success': True,
            'data': mecanicos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todoss los mecanicos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@mecapi.route('/mecanicos/<int:mecanico_id>', methods=['GET'])
def getMecanico(mecanico_id):
    mecanicodao = MecanicoDao()

    try:
        mecanico = mecanicodao.getMecanicoById(mecanico_id)

        if mecanico:
            return jsonify({
                'success': True,
                'data': mecanico,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la mecanico con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener mecanico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva mecanico
@mecapi.route('/mecanicos', methods=['POST'])
def addMecanico():
    data = request.get_json()
    mecanicodao = MecanicoDao()

    campos_requeridos = ['nombre', 'apellido']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre = data['nombre'].upper()
        apellido = data['apellido'].upper()
        mecanico_id = mecanicodao.guardarMecanico(nombre, apellido)
        if mecanico_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': mecanico_id, 'nombre': nombre, 'apellido': apellido},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la mecanico. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar mecanico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@mecapi.route('/mecanicos/<int:mecanico_id>', methods=['PUT'])
def updateMecanico(mecanico_id):
    data = request.get_json()
    mecanicodao = MecanicoDao()

    campos_requeridos = ['nombre', 'apellido']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    nombre = data['nombre']
    apellido = data['apellido']

    try:
        if mecanicodao.updateMecanico(mecanico_id, nombre.upper(), apellido.upper()):
            return jsonify({
                'success': True,
                'data': {'id': mecanico_id, 'nombre': nombre, 'apellido': apellido},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la mecanico con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar mecanico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@mecapi.route('/mecanicos/<int:mecanico_id>', methods=['DELETE'])
def deleteMecanico(mecanico_id):
    mecanicodao = MecanicoDao()

    try:
        if mecanicodao.deleteMecanico(mecanico_id):
            return jsonify({
                'success': True,
                'mensaje': f'Persona con ID {mecanico_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la mecanico con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar mecanico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
