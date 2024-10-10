from flask import current_app as app
from app.conexion.Conexion import Conexion

class MecanicoDao:

    def getMecanicos(self):
        mecanicoSQL = """
        SELECT id, nombre, apellido
        FROM mecanicos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(mecanicoSQL)
            mecanicos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': mecanico[0], 'nombre': mecanico[1], 'apellido': mecanico[2]} for mecanico in mecanicos]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las mecanicos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMecanicoById(self, id):
        mecanicoSQL = """
        SELECT id, nombre, apellido
        FROM mecanicos WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(mecanicoSQL, (id,))
            mecanicoEncontrado = cur.fetchone()  # Obtener una sola fila
            if mecanicoEncontrado:
                return {
                    "id": mecanicoEncontrado[0],
                    "nombre": mecanicoEncontrado[1],
                    "apellido": mecanicoEncontrado[2]
                }  # Retornar los datos de la mecanico
            else:
                return None  # Retornar None si no se encuentra la mecanico
        except Exception as e:
            app.logger.error(f"Error al obtener mecanico: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarMecanico(self, nombre, apellido):
        insertMecanicoSQL = """
        INSERT INTO mecanicos(nombre, apellido) VALUES(%s, %s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertMecanicoSQL, (nombre, apellido))
            mecanico_id = cur.fetchone()[0]
            con.commit()  # se confirma la inserción
            return mecanico_id

        except Exception as e:
            app.logger.error(f"Error al insertar mecanico: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateMecanico(self, id, nombre, apellido):
        updateMecanicoSQL = """
        UPDATE mecanicos
        SET nombre=%s, apellido=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateMecanicoSQL, (nombre, apellido, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar mecanico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMecanico(self, id):
        deleteMecanicoSQL = """
        DELETE FROM mecanicos
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMecanicoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar mecanico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
