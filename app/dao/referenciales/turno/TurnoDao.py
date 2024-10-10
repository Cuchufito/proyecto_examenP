from flask import current_app as app
from app.conexion.Conexion import Conexion

class TurnoDao:

    def getTurnos(self):
        turnoSQL = """
        SELECT id, dia, horario
        FROM turnos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(turnoSQL)
            turnos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': turno[0], 'dia': turno[1], 'horario': turno[2]} for turno in turnos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los turnos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTurnoById(self, id):
        turnoSQL = """
        SELECT id, dia, horario
        FROM turnos WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(turnoSQL, (id,))
            trunoEncontrado = cur.fetchone()  # Obtener una sola fila
            if trunoEncontrado:
                return {
                    "id": trunoEncontrado[0],
                    "dia": trunoEncontrado[1],
                    "horario": trunoEncontrado[2]
                }  # Retornar los datos de la persona
            else:
                return None  # Retornar None si no se encuentra la persona
        except Exception as e:
            app.logger.error(f"Error al obtener turno: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTurno(self, dia, horario):
        insertTurnoSQL = """
        INSERT INTO turnos(dia, horario) VALUES(%s, %s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertTurnoSQL, (dia, horario))
            persona_id = cur.fetchone()[0]
            con.commit()  # se confirma la inserción
            return persona_id

        except Exception as e:
            app.logger.error(f"Error al insertar turno: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateTurno(self, id, dia, horario):
        updateTurnoSQL = """
        UPDATE turnos
        SET dia=%s, horario=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTurnoSQL, (dia, horario, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar turno: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTurno(self, id):
        deleteTurnoSQL = """
        DELETE FROM turnos
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteTurnoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar truno: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
