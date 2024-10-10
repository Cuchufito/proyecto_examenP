# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ModeloDao:

    def getModelos(self):

        modeloSQL = """
        SELECT id, descripcion
        FROM modelos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(modeloSQL)
            modelos = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': modelo[0], 'descripcion': modelo[1]} for modelo in modelos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los modelos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getModeloById(self, id):

        modeloSQL = """
        SELECT id, descripcion
        FROM modelos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(modeloSQL, (id,))
            modeloEncontrada = cur.fetchone() # Obtener una sola fila
            if modeloEncontrada:
                return {
                        "id": modeloEncontrada[0],
                        "descripcion": modeloEncontrada[1]
                    }  # Retornar los datos de la tabla modelo
            else:
                return None # Retornar None si no se encuentra la tabla modelo
        except Exception as e:
            app.logger.error(f"Error al obtener el modelo: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarModelo(self, descripcion):

        insertModeloSQL = """
        INSERT INTO modelos(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertModeloSQL, (descripcion,))
            modelo_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return modelo_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar el modelo: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateModelo(self, id, descripcion):

        updateModeloSQL = """
        UPDATE modelos
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateModeloSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar el modelo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteModelo(self, id):

        updateModeloSQL = """
        DELETE FROM modelos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateModeloSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar el modelo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()