from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.marca.MarcaDao import MarcaDao

marcapi = Blueprint('marcapi', __name__)

# Trae todas los marcas de las personas
@marcapi.route('/marcas', methods=['GET'])
def getMarcas():
    marcadao = MarcaDao()

    try:
        marcas = marcadao.getMarcas()

        return jsonify({
            'success': True,
            'data': marcas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas los marcas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@marcapi.route('/marcas/<int:marca_id>', methods=['GET'])
def getMarca(marca_id):
    marcadao = MarcaDao()

    try:
        marca = marcadao.getMarcaById(marca_id)

        if marca:
            return jsonify({
                'success': True,
                'data': marca,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el marca con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener marca: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nuevo marca de la persona
@marcapi.route('/marcas', methods=['POST'])
def addMarca():
    data = request.get_json()
    marcadao = MarcaDao()

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
        marca_id = marcadao.guardarMarca(descripcion)
        if marca_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': marca_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el marca. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar marca: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@marcapi.route('/marcas/<int:marca_id>', methods=['PUT'])
def updateMarca(marca_id):
    data = request.get_json()
    marcadao = MarcaDao()

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
        if marcadao.updateMarca(marca_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': marca_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el marca con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar marca: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@marcapi.route('/marcas/<int:marca_id>', methods=['DELETE'])
def deleteMarca(marca_id):
    marcadao = MarcaDao()

    try:
        # Usar el retorno de eliminarMarca para determinar el éxito
        if marcadao.deleteMarca(marca_id):
            return jsonify({
                'success': True,
                'mensaje': f'Marca con ID {marca_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el marca con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar marca: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500