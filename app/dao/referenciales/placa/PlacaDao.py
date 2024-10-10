# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class PlacaDao:

    def getPlacas(self):

        placaSQL = """
        SELECT id, descripcion
        FROM placas
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(placaSQL)
            placas = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': placa[0], 'descripcion': placa[1]} for placa in placas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las placas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getPlacaById(self, id):

        placaSQL = """
        SELECT id, descripcion
        FROM placas WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(placaSQL, (id,))
            placaEncontrada = cur.fetchone() # Obtener una sola fila
            if placaEncontrada:
                return {
                        "id": placaEncontrada[0],
                        "descripcion": placaEncontrada[1]
                    }  # Retornar los datos de la tabla placa
            else:
                return None # Retornar None si no se encuentra la tabla placa
        except Exception as e:
            app.logger.error(f"Error al obtener la placa: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPlaca(self, descripcion):

        insertPlacaSQL = """
        INSERT INTO placas(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertPlacaSQL, (descripcion,))
            placa_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return placa_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar la placa: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updatePlaca(self, id, descripcion):

        updatePlacaSQL = """
        UPDATE placas
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePlacaSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar la placa: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deletePlaca(self, id):

        updatePlacaSQL = """
        DELETE FROM placas
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePlacaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar el placa: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()