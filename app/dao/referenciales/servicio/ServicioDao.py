# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ServicioDao:

    def getServicios(self):

        serviciosSQL = """
        SELECT id, descripcion_servicio
        FROM servicios
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(serviciosSQL)
            servicios = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': servicios[0], 'descripcion_servicio': servicios[1]} for servicios in servicios]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los servicios: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getServiciosById(self, id):

        serviciosSQL = """
        SELECT id, descripcion_servicio
        FROM servicios WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(serviciosSQL, (id,))
            servicioEncontrado = cur.fetchone() # Obtener una sola fila
            if servicioEncontrado:
                return {
                        "id": servicioEncontrado[0],
                        "descripcion_servicio": servicioEncontrado[1]
                    }  # Retornar los datos de la ciudad
            else:
                return None # Retornar None si no se encuentra el servicio
        except Exception as e:
            app.logger.error(f"Error al obtener el Servicio: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarServicio(self, descripcion_servicio):

        insertserviciosSQL = """
        INSERT INTO servicios(descripcion_servicio) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertserviciosSQL, (descripcion_servicio,))
            ciudad_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return ciudad_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar servicio: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateServicio(self, id, descripcion_servicio):

        updateServicioSQL = """
        UPDATE servicios
        SET descripcion_servicio=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateServicioSQL, (descripcion_servicio, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar servicio: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteServicio(self, id):

        updateServicioSQL = """
        DELETE FROM servicios
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateServicioSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar servicico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()