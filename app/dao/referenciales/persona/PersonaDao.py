
from flask import current_app as app
from app.conexion.Conexion import Conexion

class PersonaDao:

    def getPersonas(self):
        personaSQL = """
        SELECT id, nombre, apellido, cedula, fechanac
        FROM personas
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL)
            personas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': persona[0], 'nombre': persona[1], 'apellido': persona[2], 'cedula': persona[3], 'fechanac': persona[4]} for persona in personas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las personas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getPersonaById(self, id):
        personaSQL = """
        SELECT id, nombre, apellido, cedula, fechanac
        FROM personas WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(personaSQL, (id,))
            personaEncontrada = cur.fetchone()  # Obtener una sola fila
            if personaEncontrada:
                return {
                    "id": personaEncontrada[0],
                    "nombre": personaEncontrada[1],
                    "apellido": personaEncontrada[2],
                    "cedula": personaEncontrada[3],
                    "fechanac": personaEncontrada[4]
                }  # Retornar los datos de la persona
            else:
                return None  # Retornar None si no se encuentra la persona
        except Exception as e:
            app.logger.error(f"Error al obtener persona: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPersona(self, nombre, apellido, cedula, fechanac):
        insertPersonaSQL = """
        INSERT INTO personas(nombre, apellido, cedula, fechanac) 
        VALUES(%s, %s, %s, %s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertPersonaSQL, (nombre, apellido, cedula, fechanac))
            persona_id = cur.fetchone()[0]
            con.commit()  # Confirmar la inserción
            return persona_id

        except Exception as e:
            app.logger.error(f"Error al insertar persona: {str(e)}")
            con.rollback()  # Revertir si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updatePersona(self, id, nombre, apellido, cedula, fechanac):
        updatePersonaSQL = """
        UPDATE personas
        SET nombre=%s, apellido=%s, cedula=%s, fechanac=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePersonaSQL, (nombre.upper(), apellido.upper(), cedula, fechanac, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar persona: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deletePersona(self, id):
        deletePersonaSQL = """
        DELETE FROM personas
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deletePersonaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar persona: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
