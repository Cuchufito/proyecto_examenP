from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.proveedor.ProveedorDao import ProveedorDao

proapi = Blueprint('proapi', __name__)

# Trae todos los proveedor
@proapi.route('/proveedor', methods=['GET'])
def getProveedores():
    proveedordao =ProveedorDao()

    try:
        proveedores = proveedordao.getProveedores()

        return jsonify({
            'success': True,
            'data': proveedores,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los proveedores: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proapi.route('/proveedor/<int:proveedor_id>', methods=['GET'])
def getProveedor(proveedor_id):
    proveedorDao =ProveedorDao()

    try:
        proveedor = proveedorDao.getProveedorById(proveedor_id)

        if proveedor:
            return jsonify({
                'success': True,
                'data': proveedor,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el proveedor con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo proveedor
@proapi.route('/proveedor', methods=['POST'])
def addProveedor():
    data = request.get_json()
    proveedorDao =ProveedorDao()

    campos_requeridos = ['ruc', 'razon_social']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        ruc = data['ruc'].upper()
        razon_social = data['razon_social'].upper()
        proveedor_id = proveedorDao.guardarProveedor(ruc, razon_social)
        if proveedor_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': proveedor_id, 'ruc': ruc, 'razon_social': razon_social},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la proveedor. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proapi.route('/proveedor/<int:proveedor_id>', methods=['PUT'])
def updateProveedor(proveedor_id):
    data = request.get_json()
    proveedorDao =ProveedorDao()

    campos_requeridos = ['ruc', 'razon_social']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    ruc = data['ruc']
    razon_social = data['razon_social']

    try:
        if proveedorDao.updateProveedor(proveedor_id, ruc.upper(), razon_social.upper()):
            return jsonify({
                'success': True,
                'data': {'id': proveedor_id, 'ruc': ruc, 'razon_social': razon_social},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el proveedor con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proapi.route('/proveedor/<int:proveedor_id>', methods=['DELETE'])
def deleteProveedor(proveedor_id):
    proveedorDao =ProveedorDao()

    try:
        if proveedorDao.deleteProveedor(proveedor_id):
            return jsonify({
                'success': True,
                'mensaje': f'Proveedor con ID {proveedor_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró al proveedor con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
