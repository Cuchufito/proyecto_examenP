# app/api/recepciones_api.py
from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.recepciones.RecepcionDao import RecepcionDao

recepapi = Blueprint('recepapi', __name__)

@recepapi.route('/recepciones', methods=['GET'])
def get_recepciones():
    dao = RecepcionDao()
    try:
        recs = dao.get_all()
        return jsonify({
            'data': recs,
            'success': True,
            'message': 'Recepciones obtenidas correctamente'
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener recepciones: {e}")
        return jsonify({'success': False, 'message': 'Error al obtener recepciones'}), 500

@recepapi.route('/recepciones/<int:recepcion_id>', methods=['GET'])
def get_recepcion(recepcion_id):
    dao = RecepcionDao()
    try:
        rec = dao.get_by_id(recepcion_id)
        if rec:
            return jsonify({'data': rec, 'success': True, 'message': 'Recepción obtenida correctamente'}), 200
        return jsonify({'success': False, 'message': 'Recepción no encontrada'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener recepción: {e}")
        return jsonify({'success': False, 'message': 'Error al obtener recepción'}), 500

@recepapi.route('/recepciones', methods=['POST'])
def create_recepcion():
    data = request.get_json() or {}
    # Campos mínimos requeridos
    required = ['vehiculo_id', 'motivo_ingreso', 'kilometraje', 'nivel_combustible', 'porcentaje_combustible']
    if not all(field in data for field in required):
        return jsonify({
            'success': False,
            'message': f'Faltan campos requeridos: {", ".join(required)}'
        }), 400

    dao = RecepcionDao()
    try:
        new_id = dao.create(
            data['vehiculo_id'],
            data['motivo_ingreso'],
            data['kilometraje'],
            data['nivel_combustible'],
            data['porcentaje_combustible'],
            data.get('observaciones', ''),
            data.get('estado', 'pendiente')
        )
        if new_id:
            rec = dao.get_by_id(new_id)
            return jsonify({'data': rec, 'success': True, 'message': 'Recepción creada correctamente'}), 201
        return jsonify({'success': False, 'message': 'No se pudo crear la recepción'}), 400
    except Exception as e:
        app.logger.error(f"Error al crear recepción: {e}")
        return jsonify({'success': False, 'message': 'Error al crear recepción'}), 500

@recepapi.route('/recepciones/<int:recepcion_id>', methods=['PUT'])
def update_recepcion(recepcion_id):
    data = request.get_json() or {}
    required = ['vehiculo_id', 'motivo_ingreso', 'kilometraje', 'nivel_combustible', 'porcentaje_combustible', 'estado']
    if not all(field in data for field in required):
        return jsonify({
            'success': False,
            'message': f'Faltan campos requeridos: {", ".join(required)}'
        }), 400

    dao = RecepcionDao()
    try:
        updated = dao.update(
            recepcion_id,
            data['vehiculo_id'],
            data['motivo_ingreso'],
            data['kilometraje'],
            data['nivel_combustible'],
            data['porcentaje_combustible'],
            data.get('observaciones', ''),
            data['estado']
        )
        if updated:
            rec = dao.get_by_id(recepcion_id)
            return jsonify({'data': rec, 'success': True, 'message': 'Recepción actualizada correctamente'}), 200
        return jsonify({'success': False, 'message': 'Recepción no encontrada o no pudo actualizarse'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar recepción: {e}")
        return jsonify({'success': False, 'message': 'Error al actualizar recepción'}), 500

@recepapi.route('/recepciones/<int:recepcion_id>', methods=['DELETE'])
def delete_recepcion(recepcion_id):
    dao = RecepcionDao()
    try:
        deleted = dao.delete(recepcion_id)
        if deleted:
            return jsonify({'success': True, 'message': 'Recepción eliminada correctamente'}), 200
        return jsonify({'success': False, 'message': 'Recepción no encontrada o no pudo eliminarse'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar recepción: {e}")
        return jsonify({'success': False, 'message': 'Error al eliminar recepción'}), 500
