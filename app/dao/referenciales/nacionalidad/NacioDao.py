# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class NacioDao:

    def getNacionalidades(self):

        nacioSQL = """
        SELECT id, descripcion
        FROM nacionalidad
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(nacioSQL)
            nacionalidad = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': nacionalidad[0], 'descripcion': nacionalidad[1]} for nacionalidad in nacionalidad]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las nacionalidades: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getNacionalidadById(self, id):

        nacioSQL = """
        SELECT id, descripcion
        FROM nacionalidad WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(nacioSQL, (id,))
            nacioEncontrada = cur.fetchone() # Obtener una sola fila
            if nacioEncontrada:
                return {
                        "id": nacioEncontrada[0],
                        "descripcion": nacioEncontrada[1]
                    }  # Retornar los datos de pais
            else:
                return None # Retornar None si no se encuentra el pais
        except Exception as e:
            app.logger.error(f"Error al obtener la nacionalidad: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarNacionalidad(self, descripcion):

        insertNacioSQL = """
        INSERT INTO nacionalidad(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertNacioSQL, (descripcion,))
            nacio_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return nacio_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar la nacionalidad: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateNacionalidad(self, id, descripcion):

        updateNacioSQL = """
        UPDATE nacionalidad
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateNacioSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar nacionalidad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteNacionalidad(self, id):

        updateNacioSQL = """
        DELETE FROM nacionalidad
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateNacioSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar la Nacionalidad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()