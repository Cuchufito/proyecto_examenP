# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class EstadoServicioDao:

    def getEstadoServicio(self):

        estadoServicioSQL = """
        SELECT id, descripcion_estado
        FROM estado_servicio
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(estadoServicioSQL)
            estadoServicios = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': estadoservicio[0], 'descripcion_estado': estadoservicio[1]} for estadoservicio in estadoServicios]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los Estados del Servicio: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEstadoServicioById(self, id):

        estadoServicioSQL = """
        SELECT id, descripcion_estado
        FROM estado_servicio WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(estadoServicioSQL, (id,))
            estadoServicioEncontrado = cur.fetchone() # Obtener una sola fila
            if estadoServicioEncontrado:
                return {
                        "id": estadoServicioEncontrado[0],
                        "descripcion_estado": estadoServicioEncontrado[1]
                    }  # Retornar los datos de los estados del servicio
            else:
                return None # Retornar None si no se encuentra los estados del servicio
        except Exception as e:
            app.logger.error(f"Error al obtener el estado del Servicio: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEstadoServicio(self, descripcion_estado):

        insertEstadoServicioSQL = """
        INSERT INTO estado_servicio(descripcion_estado) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertEstadoServicioSQL, (descripcion_estado,))
            estadoservicio_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return estadoservicio_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar estado de Servicio: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateEstadoServicio(self, id, descripcion_estado):

        updateEstadoServicioSQL = """
        UPDATE estado_servicio
        SET descripcion_estado=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEstadoServicioSQL, (descripcion_estado, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar Estado del Servicio: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEstadoServicio(self, id):

        updateEstadoServicioSQL = """
        DELETE FROM estado_servicio
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEstadoServicioSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar Estado de Servicio: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()