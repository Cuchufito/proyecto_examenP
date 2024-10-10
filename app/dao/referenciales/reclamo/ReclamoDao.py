from flask import current_app as app
from app.conexion.Conexion import Conexion

class ReclamoDao:

    def getReclamos(self):
        reclamoSQL = """
        SELECT id, nombre, descripcion
        FROM reclamos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(reclamoSQL)
            reclamos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': reclamo[0], 'nombre': reclamo[1], 'descripcion': reclamo[2]} for reclamo in reclamos]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las reclamos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getReclamoById(self, id):
        reclamoSQL = """
        SELECT id, nombre, descripcion
        FROM reclamos WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(reclamoSQL, (id,))
            reclamoEncontrado = cur.fetchone()  # Obtener una sola fila
            if reclamoEncontrado:
                return {
                    "id": reclamoEncontrado[0],
                    "nombre": reclamoEncontrado[1],
                    "descripcion": reclamoEncontrado[2]
                }  # Retornar los datos de el reclamo
            else:
                return None  # Retornar None si no se encuentra el reclamo
        except Exception as e:
            app.logger.error(f"Error al obtener reclamo: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarReclamo(self, nombre, descripcion):
        insertReclamoSQL = """
        INSERT INTO reclamos(nombre, descripcion) VALUES(%s, %s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertReclamoSQL, (nombre, descripcion))
            reclamo_id = cur.fetchone()[0]
            con.commit()  # se confirma la inserción
            return reclamo_id

        except Exception as e:
            app.logger.error(f"Error al insertar reclamo: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateReclamo(self, id, nombre, descripcion):
        updateReclamoSQL = """
        UPDATE reclamos
        SET nombre=%s, descripcion=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateReclamoSQL, (nombre, descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar reclamo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteReclamo(self, id):
        deleteReclamoSQL = """
        DELETE FROM reclamos
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteReclamoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar reclamo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
