from flask import current_app as app
from app.conexion.Conexion import Conexion

class VehiculoDao:

    def getVehiculos(self):
        vehiculoSQL = """
        SELECT id, marca, modelo
        FROM vehiculos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(vehiculoSQL)
            vehiculos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': vehiculo[0], 'marca': vehiculo[1], 'modelo': vehiculo[2]} for vehiculo in vehiculos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los vehiculos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getVehiculoById(self, id):
        vehiculoSQL = """
        SELECT id, marca, modelo
        FROM vehiculos WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(vehiculoSQL, (id,))
            vehiculoEncontrado = cur.fetchone()  # Obtener una sola fila
            if vehiculoEncontrado:
                return {
                    "id": vehiculoEncontrado[0],
                    "marca": vehiculoEncontrado[1],
                    "modelo": vehiculoEncontrado[2]
                }  # Retornar los datos de la vehiculo
            else:
                return None  # Retornar None si no se encuentra la vehiculo
        except Exception as e:
            app.logger.error(f"Error al obtener vehiiculo: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarVehiculo(self, marca, modelo):
        insertvehiculoSQL = """
        INSERT INTO vehiculos(marca, modelo) VALUES(%s, %s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertvehiculoSQL, (marca, modelo))
            vehiculo_id = cur.fetchone()[0]
            con.commit()  # se confirma la inserción
            return vehiculo_id

        except Exception as e:
            app.logger.error(f"Error al insertar vehicculo: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateVehiculo(self, id, marca, modelo):
        updatevehiculoSQL = """
        UPDATE vehiculos
        SET marca=%s, modelo=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatevehiculoSQL, (marca, modelo, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar vehiculo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteVehiculo(self, id):
        deletevehiculoSQL = """
        DELETE FROM vehiculos
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deletevehiculoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar vehiculo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
