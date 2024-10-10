from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.modelo.ModeloDao import ModeloDao

modelapi = Blueprint('modelapi', __name__)

# Trae todas los modelos de las personas
@modelapi.route('/modelos', methods=['GET'])
def getModelos():
    modelodao = ModeloDao()

    try:
        modelos = modelodao.getModelos()

        return jsonify({
            'success': True,
            'data': modelos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas los modelos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@modelapi.route('/modelos/<int:modelo_id>', methods=['GET'])
def getModelo(modelo_id):
    modelodao = ModeloDao()

    try:
        modelo = modelodao.getModeloById(modelo_id)

        if modelo:
            return jsonify({
                'success': True,
                'data': modelo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el modelo con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener modelo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nuevo modelo de la persona
@modelapi.route('/modelos', methods=['POST'])
def addModelo():
    data = request.get_json()
    modelodao = ModeloDao()

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
        modelo_id = modelodao.guardarModelo(descripcion)
        if modelo_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': modelo_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el modelo. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar modelo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@modelapi.route('/modelos/<int:modelo_id>', methods=['PUT'])
def updateModelo(modelo_id):
    data = request.get_json()
    modelodao = ModeloDao()

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
        if modelodao.updateModelo(modelo_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': modelo_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el modelo con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar modelo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@modelapi.route('/modelos/<int:modelo_id>', methods=['DELETE'])
def deleteModelo(modelo_id):
    modelodao = ModeloDao()

    try:
        # Usar el retorno de eliminarModelo para determinar el éxito
        if modelodao.deleteModelo(modelo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Modelo con ID {modelo_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el modelo con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar modelo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500