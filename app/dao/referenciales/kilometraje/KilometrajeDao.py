# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class KilometrajeDao:

    def getKilometrajes(self):

        kilometrajeSQL = """
        SELECT id, descripcion
        FROM kilometrajes
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(kilometrajeSQL)
            kilometrajes = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': kilometraje[0], 'descripcion': kilometraje[1]} for kilometraje in kilometrajes]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las kilometrajes: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getKilometrajeById(self, id):

        kilometrajeSQL = """
        SELECT id, descripcion
        FROM kilometrajes WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(kilometrajeSQL, (id,))
            kilometrajeEncontrado = cur.fetchone() # Obtener una sola fila
            if kilometrajeEncontrado:
                return {
                        "id": kilometrajeEncontrado[0],
                        "descripcion": kilometrajeEncontrado[1]
                    }  # Retornar los datos de la kilometraje
            else:
                return None # Retornar None si no se encuentra la kilometraje
        except Exception as e:
            app.logger.error(f"Error al obtener kilometraje: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarKilometraje(self, descripcion):

        insertKilometrajeSQL = """
        INSERT INTO kilometrajes(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertKilometrajeSQL, (descripcion,))
            kilometraje_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return kilometraje_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar kilometraje: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateKilometraje(self, id, descripcion):

        updateKilometrajeSQL = """
        UPDATE kilometrajes
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateKilometrajeSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar kilometraje: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteKilometraje(self,id):

        updateKilometrajeSQL = """
        DELETE FROM kilometrajes
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateKilometrajeSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar kilometraje: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()