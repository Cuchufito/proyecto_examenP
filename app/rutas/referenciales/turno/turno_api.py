from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.turno.TurnoDao import TurnoDao

turapi = Blueprint('turapi', __name__)

# Trae todas los turnos
@turapi.route('/turnos', methods=['GET'])
def getturnos():
    turnodao = TurnoDao()

    try:
        turnos = turnodao.getTurnos()

        return jsonify({
            'success': True,
            'data': turnos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los turnos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@turapi.route('/turnos/<int:turno_id>', methods=['GET'])
def getTurnos(turno_id):
    turnodao = TurnoDao()

    try:
        turno = turnodao.getTurnoById(turno_id)

        if turno:
            return jsonify({
                'success': True,
                'data': turno,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el turno con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener turno: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva turno
@turapi.route('/turnos', methods=['POST'])
def addTurnos():
    data = request.get_json()
    turnodao = TurnoDao()

    campos_requeridos = ['dia', 'horario']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        dia = data['dia'].upper()
        horario = data['horario'].upper()
        turno_id = turnodao.guardarTurno(dia, horario)
        if turno_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': turno_id, 'dia': dia, 'horario': horario},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el turno. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@turapi.route('/turnos/<int:turno_id>', methods=['PUT'])
def updateTurno(turno_id):
    data = request.get_json()
    turnodao = TurnoDao()

    campos_requeridos = ['dia', 'horario']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    dia = data['dia']
    horario = data['horario']

    try:
        if turnodao.updateTurno(turno_id, dia.upper(), horario.upper()):
            return jsonify({
                'success': True,
                'data': {'id': turno_id, 'dia': dia, 'horario': horario},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el turno con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@turapi.route('/turnos/<int:turno_id>', methods=['DELETE'])
def deleteTurno(turno_id):
    turnodao = TurnoDao()

    try:
        if turnodao.deleteTurno(turno_id):
            return jsonify({
                'success': True,
                'mensaje': f'Turno con ID {turno_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el turno con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar turno: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
