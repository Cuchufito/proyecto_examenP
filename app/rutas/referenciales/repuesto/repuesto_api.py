from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.repuesto.RepuestoDao import RepuestoDao

repuapi = Blueprint('repuapi', __name__)

# Trae todas las repuestos
@repuapi.route('/repuestos', methods=['GET'])
def getRepuestos():
    repuestodao = RepuestoDao()

    try:
        repuestos = repuestodao.getRepuesto()

        return jsonify({
            'success': True,
            'data': repuestos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las repuestos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@repuapi.route('/repuestos/<int:repuesto_id>', methods=['GET'])
def getRepuesto(repuesto_id):
    repuestodao = RepuestoDao()

    try:
        repuesto = repuestodao.getRepuestoById(repuesto_id)

        if repuesto:
            return jsonify({
                'success': True,
                'data': repuesto,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el repuesto con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener repuesto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva repuesto
@repuapi.route('/repuestos', methods=['POST'])
def addRepuesto():
    data = request.get_json()
    repuestodao = RepuestoDao()

    campos_requeridos = ['repuesto', 'codigo']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        repuesto = data['repuesto'].upper()
        codigo = data['codigo'].upper()
        repuesto_id = repuestodao.guardarRepuesto(repuesto, codigo)
        if repuesto_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': repuesto_id, 'repuesto': repuesto, 'codigo': codigo},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el repuesto. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar repuesto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@repuapi.route('/repuestos/<int:repuesto_id>', methods=['PUT'])
def updateRepuesto(repuesto_id):
    data = request.get_json()
    repuestodao = RepuestoDao()

    campos_requeridos = ['repuesto', 'codigo']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    repuesto = data['repuesto']
    codigo = data['codigo']

    try:
        if repuestodao.updateRepuesto(repuesto_id, repuesto.upper(), codigo.upper()):
            return jsonify({
                'success': True,
                'data': {'id': repuesto_id, 'repuesto': repuesto, 'codigo': codigo},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el repuesto con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar repuesto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@repuapi.route('/repuestos/<int:repuesto_id>', methods=['DELETE'])
def deleteRepuesto(repuesto_id):
    repuestodao = RepuestoDao()

    try:
        if repuestodao.deleteRepuesto(repuesto_id):
            return jsonify({
                'success': True,
                'mensaje': f'Repuesto con ID {repuesto_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el repuesto con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar repuesto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
